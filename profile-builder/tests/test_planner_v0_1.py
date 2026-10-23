import json, unittest
from pathlib import Path
from profile_builder.planner import plan

ROOT=Path(__file__).resolve().parents[1]

class PlannerTests(unittest.TestCase):
    def load(self, rel):
        return json.loads((ROOT/rel).read_text(encoding='utf-8'))

    def test_ged03_replay(self):
        actual=plan(
            self.load('examples/ged03/characterization.json'),
            self.load('examples/ged03/requested_need.json'),
            self.load('registry/CAPABILITY_REGISTRY_V0_1.json')
        )
        expected=self.load('examples/ged03/expected_processing_plan.json')
        actual['canonical_sha256']=None
        self.assertEqual(actual, expected)

    def test_unknown_is_fail_closed(self):
        c={'schema_version':'ged-core-characterization/0.1','corpus_id':'UNKNOWN','container':{'media_type':'application/x-unknown','extension':'.xyz','page_count':None},'native_features':{'structured':False,'text_available':False,'image_available':False,'metadata_available':False},'privacy':{'local_only':True,'personal_data_present':False,'publication_allowed':False},'observations':{}}
        n={'schema_version':'ged-core-requested-need/0.1','need_id':'UNKNOWN','objectives':['EXTRACT_STRUCTURED_FIELDS'],'required_outputs':['unknown_output'],'quality_requirements':{'deterministic':True,'offline':True,'fail_closed':True}}
        out=plan(c,n,self.load('registry/CAPABILITY_REGISTRY_V0_1.json'))
        self.assertEqual(out['decision'],'CAPABILITY_GAP')
        self.assertEqual(out['selected_capabilities'],[])

    def test_hash_is_stable(self):
        args=(
            self.load('examples/ged03/characterization.json'),
            self.load('examples/ged03/requested_need.json'),
            self.load('registry/CAPABILITY_REGISTRY_V0_1.json')
        )
        self.assertEqual(plan(*args)['canonical_sha256'], plan(*args)['canonical_sha256'])

if __name__=='__main__':
    unittest.main()
