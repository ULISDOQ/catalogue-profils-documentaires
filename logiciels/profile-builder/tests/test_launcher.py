"""Vérifie les vraies entrées depuis l'extérieur, sans import fourni par le dépôt."""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PLAN_HASH = 'f0d7ebdde26100b90d4d4680dd1d7f58943d9429a16ea8d0d090dde22d709a68'


class LauncherTests(unittest.TestCase):
    def run_cli(self, root, cwd, *args, isolated=False):
        env = os.environ.copy()
        env.pop('PYTHONPATH', None)
        env.pop('PYTHONHOME', None)
        env['PATH'] = str(Path(sys.executable).parent) + os.pathsep + env.get('PATH', '')
        launcher = str(root / 'bin/profile-builder')
        command = [sys.executable, '-I', launcher] if isolated else [launcher]
        result = subprocess.run(command + list(args), cwd=cwd, env=env,
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 0, result.stderr)
        return json.loads(result.stdout)

    def assert_info(self, info, root):
        self.assertEqual(info['profile_builder_version'], '0.1.3')
        self.assertEqual(Path(info['default_registry']), root / 'registry/CAPABILITY_REGISTRY_V0_1.json')
        self.assertFalse(info['network_required'])
        self.assertFalse(info['llm_required'])

    def test_script_with_isolated_python_from_outside(self):
        with tempfile.TemporaryDirectory() as cwd:
            self.assert_info(self.run_cli(ROOT, cwd, 'info', isolated=True), ROOT)

    def test_executable_from_outside(self):
        with tempfile.TemporaryDirectory() as cwd:
            result = self.run_cli(ROOT, cwd, 'selftest')
            self.assertEqual(result['overall'], 'PASS')
            self.assertEqual(result['deterministic_replay_sha256'], PLAN_HASH)

    def test_manifest_archive_reconstructed_outside_checkout(self):
        manifest = json.loads((ROOT / 'DISTRIBUTION_MANIFEST_ORGANISATION_2.json').read_text())
        with tempfile.TemporaryDirectory() as temp:
            base = Path(temp)
            package = base / manifest['package_root']
            for rel, _ in manifest['files']:
                target = package / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(ROOT / rel, target)
            archive = base / 'package.tar.gz'
            with tarfile.open(archive, 'w:gz') as tar:
                tar.add(package, arcname=package.name)
            shutil.rmtree(package)
            extracted = base / 'extracted'
            with tarfile.open(archive) as tar:
                tar.extractall(extracted, filter='data')
            package = extracted / manifest['package_root']
            cwd = base / 'consumer'
            cwd.mkdir()
            self.assert_info(self.run_cli(package, cwd, 'info'), package)
            self.assertEqual(self.run_cli(package, cwd, 'selftest')['overall'], 'PASS')
            result = self.run_cli(package, cwd, 'plan',
                                  '--characterization', str(package / 'examples/ged03/characterization.json'),
                                  '--need', str(package / 'examples/ged03/requested_need.json'))
            expected = json.loads((package / 'examples/ged03/expected_processing_plan.json').read_text())
            self.assertEqual(result['canonical_sha256'], PLAN_HASH)
            result['canonical_sha256'] = None
            self.assertEqual(result, expected)
