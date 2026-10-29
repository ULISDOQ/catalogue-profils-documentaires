#!/usr/bin/env python3
"""Exécute les contrôles du dépôt sans source privée ni accès réseau."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
SUITES = [
    ('Cohérence des verticales', ROOT, ['-m', 'unittest', 'discover', '-s', 'logiciels/verification/tests', '-v']),
    ('Client TAG', ROOT / 'logiciels/client', ['test_tag_candidate.py']),
    ('Adaptateur facture', ROOT / 'logiciels/client', ['-m', 'unittest', 'discover', '-s', 'tests', '-p', 'test_invoice_adapter.py', '-v']),
    ('Profile Builder', ROOT / 'logiciels/profile-builder', ['-m', 'unittest', 'discover', '-s', 'tests', '-v']),
    ('Autocontrôle du Builder', ROOT / 'logiciels/profile-builder', ['-m', 'ulisdoq_profile_builder', 'selftest']),
    ('Escalade consommateur', ROOT, ['-m', 'unittest', 'discover', '-s', 'logiciels/escalade-consommateur/tests', '-v']),
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
