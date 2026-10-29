"""Recette avec invoice2data réel dans son environnement déclaré ; fixture synthétique."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ADAPTER = Path(__file__).resolve().parents[1] / 'extract.py'
TEXT = 'ULISDOQ FACTURE TEST\nFACTURE N TEST-001\nDU 01/01/2026\nMontant facture (EUR) 42,00\n'
TEMPLATE = r'''issuer: ULISDOQ-VERIFY
keywords:
  - 'ULISDOQ FACTURE TEST'
fields:
  invoice_number: 'FACTURE\s+N\s+(TEST-[0-9]+)'
  date: 'DU\s+(\d{2}/\d{2}/\d{4})'
  amount: 'Montant\s+facture\s+\(EUR\)\s+(\d+[,.]\d{2})'
required_fields:
  - invoice_number
  - date
  - amount
options:
  currency: EUR
  decimal_separator: ','
  date_formats:
    - '%d/%m/%Y'
'''


def synthetic_pdf(path):
    # PDF minimal autonome : police standard, quatre lignes, table xref exacte.
    lines = [line.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)') for line in TEXT.splitlines()]
    stream = ('BT /F1 12 Tf 40 780 Td 18 TL ' + ' T* '.join('(' + line + ') Tj' for line in lines) + ' ET').encode()
    objects = [b'<< /Type /Catalog /Pages 2 0 R >>',
               b'<< /Type /Pages /Kids [3 0 R] /Count 1 >>',
               b'<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>',
               b'<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>',
               b'<< /Length ' + str(len(stream)).encode() + b' >>\nstream\n' + stream + b'\nendstream']
    pdf = b'%PDF-1.4\n'
    offsets = [0]
    for i, obj in enumerate(objects, 1):
        offsets.append(len(pdf))
        pdf += str(i).encode() + b' 0 obj\n' + obj + b'\nendobj\n'
    xref = len(pdf)
    pdf += b'xref\n0 6\n0000000000 65535 f \n'
    pdf += b''.join(f'{offset:010d} 00000 n \n'.encode() for offset in offsets[1:])
    pdf += b'trailer\n<< /Size 6 /Root 1 0 R >>\nstartxref\n' + str(xref).encode() + b'\n%%EOF\n'
    path.write_bytes(pdf)


class InvoiceIntegrationTests(unittest.TestCase):
    def run_reader(self, reader, pdf=False):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            document = root / ('invoice.pdf' if pdf else 'invoice.txt')
            if pdf:
                synthetic_pdf(document)
            else:
                document.write_text(TEXT)
            templates = root / 'templates'
            templates.mkdir()
            (templates / 'synthetic.yml').write_text(TEMPLATE)
            result = subprocess.run([sys.executable, '-I', str(ADAPTER), str(document), '--templates', str(templates), '--reader', reader],
                                    cwd=root, capture_output=True, text=True, timeout=30)
            return result.returncode, json.loads(result.stdout)

    def assert_fields(self, result):
        self.assertEqual(result['status'], 'EXTRACTED_UNVERIFIED')
        self.assertEqual(result['data']['invoice_number'], 'TEST-001')
        self.assertEqual(result['data']['date'], '2026-01-01T00:00:00')
        self.assertEqual(result['data']['amount'], 42.0)
        self.assertEqual(result['data']['currency'], 'EUR')

    def test_real_text_reader(self):
        rc, result = self.run_reader('text')
        self.assertEqual(rc, 0, result)
        self.assert_fields(result)

    def test_real_pdftotext_reader(self):
        rc, result = self.run_reader('pdftotext', pdf=True)
        self.assertEqual(rc, 0, result)
        self.assert_fields(result)

    def test_unknown_reader(self):
        rc, result = self.run_reader('unknown_reader')
        self.assertEqual(rc, 2)
        self.assertEqual(result['status'], 'ERROR')
        self.assertIn('Unsupported local reader', result['reason'])
