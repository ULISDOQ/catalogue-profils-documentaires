import copy
import runpy
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NS = runpy.run_path(str(ROOT / "bin" / "ulisdoq-escalation"))
load = NS["load"]
validate_request = NS["validate_request"]
validate_cycle = NS["validate_cycle"]
accept_request = NS["accept_request"]

REQUEST_ID = "ULISDOQ-REQ-GEDREAL-20261024T213000Z-001"
REQUEST = ROOT / "demandes" / REQUEST_ID / "request.json"
RECEIPT = ROOT / "accuses" / REQUEST_ID / "receipt.json"
RESULT = ROOT / "resultats" / REQUEST_ID / "result.json"


class ConsumerEscalationV1Tests(unittest.TestCase):
    def test_ged04_real_cycle_is_coherent(self):
        out = validate_cycle(load(REQUEST), load(RECEIPT), load(RESULT))
        self.assertEqual(out["status"], "PASS")
        self.assertEqual(out["acceptance_status"], "ACCEPTED")
        self.assertEqual(out["result_status"], "COMPLETED")
        self.assertEqual(out["capability_decision"], "NEW_PROFILE_CANDIDATE_REQUIRED")
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
        self.assertEqual(result["next_action"]["target_ref"], "ULISDOQ-PROFILE-GED04-MOTORCYCLE-INSURANCE-SPECIAL-TERMS-CANDIDATE@0.1.0")
        profile = load(ROOT.parent / result["produced_refs"]["profile_path"])
        self.assertEqual(profile["profile_id"], result["produced_refs"]["profile_id"])
        self.assertFalse(profile["production_qualified"])

    def test_identical_request_is_not_productively_accepted_twice(self):
        request = load(REQUEST)
        ledger = {"schema": "ULISDOQ_ESCALATION_ACCEPTANCE_LEDGER_V1", "accepted": {}}
        first, first_changed = accept_request(
            request,
            "3bac3126e552fb6227e0ac041b2c636e884423c2",
            "2026-10-24T21:35:00Z",
            ledger,
        )
        second, second_changed = accept_request(
            request,
            "3bac3126e552fb6227e0ac041b2c636e884423c2",
            "2026-10-24T21:36:00Z",
            ledger,
        )
        self.assertTrue(first_changed)
        self.assertEqual(first["acceptance_status"], "ACCEPTED")
        self.assertFalse(second_changed)
        self.assertEqual(second["acceptance_status"], "DUPLICATE_ALREADY_ACCEPTED")


if __name__ == "__main__":
    unittest.main()
