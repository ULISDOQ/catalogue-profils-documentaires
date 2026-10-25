#!/usr/bin/env python3
"""Exécute les contrôles du dépôt sans source privée ni accès réseau."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SUITES = [
    ('Cohérence des verticales', ROOT, ['-m', 'unittest', 'discover', '-s', 'tests', '-v']),
    ('Client TAG', ROOT / 'client', ['test_tag_candidate.py']),
    ('Profile Builder', ROOT / 'profile-builder', ['-m', 'unittest', 'discover', '-s', 'tests', '-v']),
    ('Autocontrôle du Builder', ROOT / 'profile-builder', ['-m', 'ulisdoq_profile_builder', 'selftest']),
    ('Escalade consommateur', ROOT, ['-m', 'unittest', 'discover', '-s', 'escalade-consommateur/tests', '-v']),
]


def main():
    failed = []
    for name, cwd, args in SUITES:
        print('\n' + name, flush=True)
        result = subprocess.run([sys.executable, *args], cwd=cwd)
        if result.returncode:
            failed.append(name)
    print('\n' + ('FAIL : ' + ', '.join(failed) if failed else 'PASS : toutes les suites'))
    return int(bool(failed))


if __name__ == '__main__':
    raise SystemExit(main())
