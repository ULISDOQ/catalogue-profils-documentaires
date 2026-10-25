"""Cohérence des ressources après rangement ; aucune source privée requise.

Exécution : python3 -m unittest discover -s tests -v
Les validations JSON Schema nécessitent la dépendance jsonschema déclarée.
"""
import ast
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest
import zlib

ROOT = Path(__file__).resolve().parents[1]
FROZEN = 'experiences/administration-droits/GED-03/preuves/FROZEN_RESULTS_BUNDLE_001.json'
MAPPING = 'experiences/administration-droits/GED-03/preuves/CORRESPONDANCE_CHEMINS_HISTORIQUES.json'


def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))


def strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, list):
        for value in obj:
            yield from strings(value)
    elif isinstance(obj, dict):
        for value in obj.values():
            yield from strings(value)


class CoherenceVerticales(unittest.TestCase):
    def test_01_no_active_obsolete_paths(self):
        obsolete = 'exper' + 'iments/'
        roots = ('experiences/', 'client/', 'ULISTAG/', 'catalogue/',
                 'profile-builder/', 'deployment/', 'project/', 'escalade-consommateur/')
        pattern = re.compile(r'(?<![\w/])(?:' + '|'.join(re.escape(r) for r in roots) + r')[^\s`"\'<>),;\]]+')
        errors = []
        for p in ROOT.rglob('*'):
            if not p.is_file() or '.git' in p.parts or '__pycache__' in p.parts:
                continue
            rel = p.relative_to(ROOT).as_posix()
            if rel in (FROZEN, MAPPING):
                continue
            try:
                text = p.read_text(encoding='utf-8')
            except UnicodeDecodeError:
                continue
            if obsolete in text:
                errors.append(rel + ': obsolete root')
            for m in pattern.finditer(text):
                target = m[0].rstrip('.:').split('#')[0]
                if any(marker in target for marker in ('...', '*', 'GED-N')):
                    continue
                # Schema identifiers and conceptual notation are not paths.
                if target in ('deployment/0.1', 'ULISTAG/TAG'):
                    continue
                if not (ROOT / target).exists():
                    errors.append(rel + ': ' + target)
        self.assertEqual(errors, [])

    def test_02_historical_evidence_is_immutable_and_resolvable(self):
        mapping = load(MAPPING)
        self.assertEqual(hashlib.sha256((ROOT / FROZEN).read_bytes()).hexdigest(), mapping['frozen_sha256'])
        historical = load(FROZEN)
        for old, new in mapping['paths'].items():
            self.assertIn(old, list(strings(historical)))
            self.assertTrue((ROOT / new).is_file(), new)

    def test_03_profile_registry_and_blob_bindings(self):
        for entry in load('project/PROFILE_REGISTRY_V0_1.json')['profiles']:
            p = ROOT / entry['profile_path']
            data = p.read_bytes()
            digest = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            self.assertEqual(digest, entry['profile_git_blob_sha'])
            profile = json.loads(data)
            self.assertEqual(profile['profile_id'], entry['profile_id'])
            for value in strings(entry):
                if value.startswith(('client/', 'ULISTAG/', 'experiences/')):
                    self.assertTrue((ROOT / value).is_file(), value)

    def test_04_capability_registry_resources(self):
        for cap in load('profile-builder/registry/CAPABILITY_REGISTRY_V0_1.json')['capabilities']:
            for value in [cap.get('adapter_path'), *cap.get('evidence_refs', [])]:
                if value:
                    self.assertTrue((ROOT / value).is_file(), value)

    def test_05_ged01_relative_resources(self):
        base = ROOT / 'experiences/factures/GED-01'
        for rel, keys in [('profils/profil_facture_fictive_001.json', ['source_fixture', 'expected_fields_ref']),
                          ('ulistag/reference_v0_1.json', ['profile_ref'])]:
            p = base / rel
            data = json.loads(p.read_text())
            for key in keys:
                self.assertTrue((p.parent / data[key]).is_file(), data[key])
        self.assertTrue((base / load('experiences/factures/GED-01/tests/cas_ged01.json')['cases'][0]['input']).is_file())

    def test_06_ged02_visual_reference_integrity(self):
        base = ROOT / 'experiences/impots-finances/GED-02/ulistag'
        manifest = json.loads((base / 'reference_visual_v0_1_manifest.json').read_text())['reference_artifact']
        packed = base64.b64decode(''.join((base / p).read_text().strip() for p in manifest['parts']), validate=True)
        self.assertEqual(hashlib.sha256(packed).hexdigest(), manifest['compressed_sha256'])
        raw = zlib.decompress(packed)
        self.assertEqual(len(raw), manifest['size_bytes'])
        self.assertEqual(hashlib.sha256(raw).hexdigest(), manifest['sha256'])
        json.loads(raw)

    def test_07_ged02_frozen_extraction_schema_and_oracle(self):
        from jsonschema import validate
        base = 'experiences/impots-finances/GED-02/'
        extracted = load(base + 'phase2-reentree/preuves/S11_PROFILE_DRIVEN_EXTRACTED_FROZEN.json')
        validate(extracted, load(base + 'extraction/semantic_extraction_schema_v0_1.json'))
        oracle = load(base + 'phase2-reentree/preuves/S11_DGFIP_SYNTHETIC_GROUND_TRUTH.json')
        observed = {f['official_id']: f['value'] for f in extracted['fields'] if f.get('status') == 'VALUE'}
        differences = {key: (observed.get(key), value)
                       for key, value in oracle['fiscal_values_by_official_line'].items()
                       if observed.get(key) != value}
        # Preserve the documented phase-2 debt; never relabel the extraction as exact.
        self.assertEqual(differences, {'420': (591, 5910)})
        debt = (ROOT / base / 'profils/DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001.md').read_text()
        self.assertIn('5910', debt)
        self.assertIn('PRODUCTION_QUALIFICATION=NO', debt)

    def test_08_ged03_resolver_and_corpus_replay(self):
        from jsonschema import validate
        spec = importlib.util.spec_from_file_location('eml', ROOT / 'client/eml_extract_v0_1.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        base = 'experiences/administration-droits/GED-03/'
        profile_path = ROOT / base / 'profils/eml_candidate.json'
        profile = json.loads(profile_path.read_text())
        schema = load(base + 'contrats/normalized_eml_schema_v0_1.json')
        for value in strings(profile):
            if value.startswith('../'):
                self.assertTrue((profile_path.parent / value).is_file(), value)
        result = subprocess.run([sys.executable, str(ROOT / 'client/profile_resolver_v0_1.py'),
                                 '--registry', str(ROOT / 'project/PROFILE_REGISTRY_V0_1.json'),
                                 '--media-type', 'message/rfc822', '--extension', '.eml'], capture_output=True, text=True, check=True)
        resolved = json.loads(result.stdout)
        self.assertEqual(resolved['status'], 'MATCH')
        self.assertTrue((ROOT / resolved['profiles'][0]['profile_path']).is_file())
        oracle = load(base + 'corpus/GROUND_TRUTH_V0_1.json')['specimens']
        for specimen, expected in oracle.items():
            output = module.normalize(ROOT / base / 'corpus' / (specimen + '.eml'), profile)
            output['traceability']['schema_validated'] = True
            validate(output, schema)
            self.assertEqual(output['parse_status'], expected['expected_status'], specimen)
            for field in ('message_id', 'subject', 'from', 'to', 'cc', 'body_html_present'):
                if field in expected:
                    self.assertEqual(output['message'][field], expected[field], specimen + ':' + field)
            if 'attachments' in expected:
                self.assertEqual(len(output['attachments']), len(expected['attachments']))
                for actual, wanted in zip(output['attachments'], expected['attachments']):
                    for key, value in wanted.items():
                        self.assertEqual(actual[key], value)
            if 'decoded_subject' in expected:
                self.assertEqual(output['message']['subject'], expected['decoded_subject'])
            if 'from_address' in expected:
                self.assertEqual(output['message']['from'], [expected['from_address']])
            if 'attachment_filename' in expected:
                self.assertEqual(output['attachments'][0]['filename'], expected['attachment_filename'])
                self.assertEqual(output['attachments'][0]['content_type'], expected['attachment_content_type'])

    def test_09_ged05_catalogue_to_profile_and_grammar(self):
        for entry in load('catalogue/index.json')['profiles']:
            profile = load(entry['path'])
            self.assertEqual(profile['profile_id'], entry['profile_id'])
            self.assertEqual(profile['profile_version'], entry['version'])
            self.assertEqual(profile['status'], entry['status'])
            base = (ROOT / entry['path']).parent
            for key in ('grammar_ref', 'qualification_ref', 'evidence_ref'):
                self.assertTrue((base / profile[key]).is_file())
            json.loads((base / profile['grammar_ref']).read_text())
            self.assertFalse(entry['automatically_selectable'])
            self.assertFalse(profile['production_qualified'])

    def test_10_deployment_schema_binding(self):
        p = ROOT / 'deployment/ubuntu/complete-v0_1/verify_complete.py'
        tree = ast.parse(p.read_text())
        binding = next(n.value for n in ast.walk(tree) if isinstance(n, ast.Assign)
                       and any(isinstance(t, ast.Name) and t.id == 'schema_path' for t in n.targets))
        self.assertIsInstance(binding, ast.BinOp)
        self.assertTrue((ROOT / ast.literal_eval(binding.right)).is_file())
        inventory = load('deployment/ubuntu/complete-v0_1/capability_inventory.json')
        for value in strings(inventory):
            if value.startswith(('client/', 'ULISTAG/', 'experiences/')):
                self.assertTrue((ROOT / value).is_file(), value)

    def test_11_markdown_relative_links(self):
        errors = []
        for p in ROOT.rglob('*.md'):
            if '.git' in p.parts:
                continue
            for value in re.findall(r'\]\(([^)]+)\)', p.read_text()):
                if '://' in value or value.startswith('#'):
                    continue
                target = value.split('#')[0]
                if target and not (p.parent / target).exists():
                    errors.append(str(p.relative_to(ROOT)) + ': ' + target)
        self.assertEqual(errors, [])

    def test_12_current_builder_distribution(self):
        manifest = load('profile-builder/DISTRIBUTION_MANIFEST_0_1_2.json')
        self.assertEqual(manifest['profile_builder_version'], '0.1.2')
        self.assertEqual(manifest['source_ref'], 'v' + (ROOT / 'VERSION').read_text().strip())
        self.assertEqual(len(manifest['files']), len({path for path, _ in manifest['files']}))
        for path, expected in manifest['files']:
            data = (ROOT / 'profile-builder' / path).read_bytes()
            observed = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
            self.assertEqual(observed, expected, path)
        self.assertTrue((ROOT / 'profile-builder' / manifest['entrypoint']).is_file())


if __name__ == '__main__':
    unittest.main()
