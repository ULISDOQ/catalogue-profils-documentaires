import copy
import json
import unittest
from pathlib import Path
from unittest import mock

from ulisdoq_profile_builder.planner import plan

ROOT = Path(__file__).resolve().parents[1]


class MatcherSelection011Tests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT / rel).read_text(encoding="utf-8"))

    def registry(self):
        return self.load("registry/CAPABILITY_REGISTRY_V0_1.json")

    def characterization(self, **observations):
        return {
            "schema_version": "ged-core-characterization/0.1",
            "corpus_id": "MATCHER_SELECTION_TEST",
            "container": {
                "media_type": "application/pdf",
                "extension": ".pdf",
                "page_count": 4,
            },
            "native_features": {
                "structured": False,
                "text_available": True,
                "image_available": True,
                "metadata_available": True,
            },
            "privacy": {
                "local_only": True,
                "personal_data_present": False,
                "publication_allowed": False,
            },
            "observations": observations,
        }

    def need(self):
        return {
            "schema_version": "ged-core-requested-need/0.1",
            "need_id": "MATCH_DOCUMENT",
            "objectives": ["RECOGNIZE_DOCUMENT_FAMILY"],
            "required_outputs": ["document_match_candidate"],
            "quality_requirements": {
                "deterministic": True,
                "offline": True,
                "fail_closed": True,
            },
        }

    def test_T1_ged03_regression_exact(self):
        actual = plan(
            self.load("examples/ged03/characterization.json"),
            self.load("examples/ged03/requested_need.json"),
            self.registry(),
        )
        expected = self.load("examples/ged03/expected_processing_plan.json")
        expected_hash = "f0d7ebdde26100b90d4d4680dd1d7f58943d9429a16ea8d0d090dde22d709a68"
        self.assertEqual(actual["canonical_sha256"], expected_hash)
        actual_without_hash = dict(actual)
        actual_without_hash["canonical_sha256"] = None
        self.assertEqual(actual_without_hash, expected)

    def test_T1b_historical_plan_hash_is_reproducible(self):
        # The historical distribution used this exact limitation string.
        # Preserve its hash separately from the corrected current example.
        registry = copy.deepcopy(self.registry())
        native = next(c for c in registry['capabilities']
                      if c['capability_id'] == 'NATIVE_MIME_EMAIL_EXTRACTION_V0.1')
        native['limits'][0] = 'Synthetic GED-03 corpus only'
        actual = plan(self.load('examples/ged03/characterization.json'),
                      self.load('examples/ged03/requested_need.json'), registry)
        self.assertEqual(actual['canonical_sha256'],
                         'f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1')
        expected = self.load('examples/ged03/expected_processing_plan.json')
        expected['limits'][0] = 'Synthetic GED-03 corpus only'
        actual['canonical_sha256'] = None
        self.assertEqual(actual, expected)

    def test_T2_anchor_graph_only_eligible(self):
        out = plan(
            self.characterization(
                stable_text_anchors=True,
                normalized_geometry=True,
                renderable_pages=False,
            ),
            self.need(),
            self.registry(),
        )
        self.assertEqual(out["decision"], "PROFILE_CANDIDATE_PRODUCED")
        self.assertEqual(
            [x["capability_id"] for x in out["selected_capabilities"]],
            ["ULISTAG-ANCHOR-GRAPH-V0.1"],
        )
        self.assertIn("PLANNING_ONLY_PROFILE_NOT_MATERIALIZED", out["limits"])

    def test_T3_visual_only_eligible(self):
        out = plan(
            self.characterization(
                stable_text_anchors=False,
                normalized_geometry=False,
                renderable_pages=True,
            ),
            self.need(),
            self.registry(),
        )
        self.assertEqual(out["decision"], "PROFILE_CANDIDATE_PRODUCED")
        self.assertEqual(
            [x["capability_id"] for x in out["selected_capabilities"]],
            ["ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC"],
        )

    def test_T4_both_eligible_lowest_cost_wins(self):
        out = plan(
            self.characterization(
                stable_text_anchors=True,
                normalized_geometry=True,
                renderable_pages=True,
            ),
            self.need(),
            self.registry(),
        )
        self.assertEqual(
            [x["capability_id"] for x in out["selected_capabilities"]],
            ["ULISTAG-ANCHOR-GRAPH-V0.1"],
        )
        visual = next(
            x for x in out["excluded_capabilities"]
            if x["capability_id"] == "ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC"
        )
        self.assertIn("higher than selected cost_rank=40", visual["reason"])

    def test_T5_equal_lowest_cost_is_ambiguous(self):
        registry = copy.deepcopy(self.registry())
        for cap in registry["capabilities"]:
            if cap["capability_id"] == "ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC":
                cap["cost_rank"] = 40
        out = plan(
            self.characterization(
                stable_text_anchors=True,
                normalized_geometry=True,
                renderable_pages=True,
            ),
            self.need(),
            registry,
        )
        self.assertEqual(out["decision"], "AMBIGUOUS")
        self.assertEqual(out["selected_capabilities"], [])
        self.assertEqual(out["unsatisfied_requirements"], ["document_match_candidate"])
        self.assertTrue(
            any(x.startswith("AMBIGUOUS_EQUAL_COST_MATCHERS:") for x in out["limits"])
        )

    def test_T6_neither_eligible_remains_capability_gap(self):
        out = plan(
            self.characterization(
                stable_text_anchors=False,
                normalized_geometry=False,
                renderable_pages=False,
            ),
            self.need(),
            self.registry(),
        )
        self.assertEqual(out["decision"], "CAPABILITY_GAP")
        self.assertEqual(out["selected_capabilities"], [])
        self.assertEqual(out["unsatisfied_requirements"], ["document_match_candidate"])

    def test_T7_deterministic_and_does_not_execute_matcher(self):
        registry = copy.deepcopy(self.registry())
        for cap in registry["capabilities"]:
            if cap.get("class") in {"STRUCTURAL_MATCHER", "VISUAL_MATCHER"}:
                cap["adapter_path"] = "/must/not/be/read/or/executed.py"
        c = self.characterization(
            stable_text_anchors=False,
            normalized_geometry=False,
            renderable_pages=True,
        )
        with mock.patch("builtins.open", side_effect=AssertionError("runtime access forbidden")):
            first = plan(c, self.need(), registry)
            second = plan(c, self.need(), registry)
        self.assertEqual(first, second)
        self.assertEqual(first["canonical_sha256"], second["canonical_sha256"])


if __name__ == "__main__":
    unittest.main()
