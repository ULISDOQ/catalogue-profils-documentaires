import copy
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = runpy.run_path(str(ROOT / "bin" / "ulisdoq-escalation"))
load = NS["load"]
validate_request = NS["validate_request"]
validate_cycle = NS["validate_cycle"]

REQUEST_ID = "ULISDOQ-REQ-GEDREAL-20261024T213000Z-001"
REQUEST = ROOT / "requests" / REQUEST_ID / "request.json"
RECEIPT = ROOT / "receipts" / REQUEST_ID / "receipt.json"
RESULT = ROOT / "results" / REQUEST_ID / "result.json"


class ConsumerEscalationV1Tests(unittest.TestCase):
    def test_ged04_real_cycle_is_coherent(self):
        out = validate_cycle(load(REQUEST), load(RECEIPT), load(RESULT))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["acceptance_status"], "ACCEPTED")
        self.assertEqual(out["result_status"], "NEEDS_MORE_EVIDENCE")
        self.assertEqual(out["capability_decision"], "SOURCE_EVIDENCE_REQUIRED")
        self.assertEqual(out["next_action"]["action"], "PROVIDE_ADDITIONAL_EVIDENCE")

    def test_private_material_declaration_is_rejected(self):
        request = copy.deepcopy(load(REQUEST))
        request["confidentiality"]["source_document"] = "INCLUDED"
        with self.assertRaisesRegex(ValueError, "CONFIDENTIALITY_BOUNDARY_VIOLATION"):
            validate_request(request)

    def test_correlation_mismatch_is_rejected(self):
        request = load(REQUEST)
        receipt = copy.deepcopy(load(RECEIPT))
        result = load(RESULT)
        receipt["correlation_id"] = "WRONG"
        with self.assertRaisesRegex(ValueError, "RECEIPT_CORRELATION_ID_MISMATCH"):
            validate_cycle(request, receipt, result)

    def test_result_gives_consumer_direct_reentry(self):
        result = load(RESULT)
        self.assertEqual(result["next_action"]["action"], "PROVIDE_ADDITIONAL_EVIDENCE")
        self.assertTrue(result["next_action"]["requirement"])
        self.assertIsNone(result["next_action"]["target_ref"])


if __name__ == "__main__":
    unittest.main()
