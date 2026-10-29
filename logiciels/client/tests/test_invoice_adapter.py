"""Contrat de l'adaptateur sans installer les moteurs dans l'environnement de test."""
from contextlib import redirect_stdout
from datetime import date
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('invoice_adapter', Path(__file__).resolve().parents[1] / 'extract.py')
adapter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(adapter)


class InvoiceAdapterTests(unittest.TestCase):
    def invoke(self, reader, engine_result=None, import_error=None):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            document = root / 'invoice.txt'
            document.write_text('SYNTHETIC INVOICE')
            templates = root / 'templates'
            templates.mkdir()
            engine = ModuleType('invoice2data')
            engine.extract_data = lambda document, templates, input_module: self.extract(input_module, engine_result)
            loader = ModuleType('invoice2data.extract.loader')
            loader.read_templates = lambda path: [{'issuer': 'SYNTHETIC'}]
            self.reader = SimpleNamespace(to_text=lambda path: 'SYNTHETIC INVOICE')
            out = io.StringIO()
            with patch.dict(sys.modules, {'invoice2data': engine, 'invoice2data.extract.loader': loader}), \
                 patch.object(sys, 'argv', ['extract.py', str(document), '--templates', str(templates), '--reader', reader]), \
                 patch.object(adapter, 'import_module', return_value=self.reader, side_effect=import_error), \
                 redirect_stdout(out):
                rc = adapter.main()
            return rc, json.loads(out.getvalue())

    def extract(self, input_module, result):
        self.assertIs(input_module, self.reader)
        self.assertTrue(callable(input_module.to_text))
        return result

    def test_reader_module_reaches_engine_and_dates_are_json(self):
        rc, result = self.invoke('text', {'invoice_number': 'TEST-001', 'date': date(2026, 1, 1), 'amount': 42.0})
        self.assertEqual(rc, 0)
        self.assertEqual(result['status'], 'EXTRACTED_UNVERIFIED')
        self.assertEqual(result['data']['date'], '2026-01-01')
        self.assertEqual(result['data']['amount'], 42.0)

    def test_unknown_reader_is_json_error(self):
        rc, result = self.invoke('unknown_reader')
        self.assertEqual(rc, 2)
        self.assertEqual(result['status'], 'ERROR')
        self.assertIn('Unsupported local reader', result['reason'])

    def test_unavailable_reader_is_json_error(self):
        rc, result = self.invoke('pdfminer', import_error=ModuleNotFoundError('pdfminer missing'))
        self.assertEqual(rc, 2)
        self.assertEqual(result['error_type'], 'ModuleNotFoundError')
        self.assertIn('pdfminer missing', result['reason'])

    def test_no_match_keeps_status_and_exit_code(self):
        rc, result = self.invoke('text', False)
        self.assertEqual(rc, 1)
        self.assertEqual(result['status'], 'NO_MATCH')
        self.assertIsNone(result['data'])

    def test_pdfminer_reader_alias(self):
        reader = SimpleNamespace(to_text=lambda path: '')
        with patch.object(adapter, 'import_module', return_value=reader) as load:
            self.assertIs(adapter.resolve_reader('pdfminer'), reader)
        load.assert_called_once_with('invoice2data.input.pdfminer_wrapper')

    def test_reader_without_callable_to_text_is_rejected(self):
        with patch.object(adapter, 'import_module', return_value=SimpleNamespace(to_text=None)):
            with self.assertRaisesRegex(RuntimeError, 'to_text'):
                adapter.resolve_reader('text')

    def test_network_reader_is_not_a_local_reader(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported local reader'):
            adapter.resolve_reader('gvision')
