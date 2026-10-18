import unittest
from tag_candidate import make_tag

class TagCandidateTests(unittest.TestCase):
    def test_order_independent(self):
        a = make_tag("invoice", ["FACTURE", "Total"])
        b = make_tag("invoice", ["total", "facture"])
        self.assertEqual(a["tag_id"], b["tag_id"])

    def test_family_separation(self):
        self.assertNotEqual(make_tag("invoice", ["2044"])["tag_id"],
                            make_tag("tax_declaration_form", ["2044"])["tag_id"])

    def test_reject_empty(self):
        with self.assertRaises(ValueError):
            make_tag("invoice", [" "])

if __name__ == "__main__":
    unittest.main()
