from __future__ import annotations
import argparse, json
from pathlib import Path
from . import __version__
from .planner import plan, MACHINE_VERSION, RULESET_VERSION

BASE=Path(__file__).resolve().parent.parent
DEFAULT_REGISTRY=BASE/'registry'/'CAPABILITY_REGISTRY_V0_1.json'

def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def cmd_info(_):
    print(json.dumps({
        'profile_builder_version':__version__,
        'ged_core_machine_version':MACHINE_VERSION,
        'ruleset_version':RULESET_VERSION,
        'default_registry':str(DEFAULT_REGISTRY),
        'network_required':False,
        'llm_required':False
    }, indent=2))

def cmd_plan(args):
    result=plan(load(args.characterization), load(args.need), load(args.registry or DEFAULT_REGISTRY))
    text=json.dumps(result, ensure_ascii=False, indent=2)+'\n'
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text, end='')
    return 0 if result['decision'] != 'CAPABILITY_GAP' else 3

def _cmp(x):
    y=dict(x)
    y['canonical_sha256']=None
    return y

def cmd_selftest(_):
    actual=plan(
        load(BASE/'examples/ged03/characterization.json'),
        load(BASE/'examples/ged03/requested_need.json'),
        load(DEFAULT_REGISTRY)
    )
    expected=load(BASE/'examples/ged03/expected_processing_plan.json')
    ok1=_cmp(actual)==_cmp(expected)
    c={
        'schema_version':'ged-core-characterization/0.1',
        'corpus_id':'SELFTEST_UNKNOWN',
        'container':{'media_type':'application/x-unknown','extension':'.xyz','page_count':None},
        'native_features':{'structured':False,'text_available':False,'image_available':False,'metadata_available':False},
        'privacy':{'local_only':True,'personal_data_present':False,'publication_allowed':False},
        'observations':{}
    }
    n={
        'schema_version':'ged-core-requested-need/0.1',
        'need_id':'SELFTEST_UNKNOWN_NEED',
        'objectives':['EXTRACT_STRUCTURED_FIELDS'],
        'required_outputs':['unknown_output'],
        'quality_requirements':{'deterministic':True,'offline':True,'fail_closed':True}
    }
    unk=plan(c,n,load(DEFAULT_REGISTRY))
    ok2=unk['decision']=='CAPABILITY_GAP' and not unk['selected_capabilities']
    out={
        'ged03_replay':'PASS' if ok1 else 'FAIL',
        'unknown_fail_closed':'PASS' if ok2 else 'FAIL',
        'deterministic_replay_sha256':actual['canonical_sha256'],
        'overall':'PASS' if ok1 and ok2 else 'FAIL'
    }
    print(json.dumps(out, indent=2))
    return 0 if out['overall']=='PASS' else 1

def main(argv=None):
    p=argparse.ArgumentParser(prog='profile-builder')
    sub=p.add_subparsers(dest='command', required=True)
    s=sub.add_parser('info')
    s.set_defaults(func=cmd_info)
    s=sub.add_parser('plan')
    s.add_argument('--characterization', required=True)
    s.add_argument('--need', required=True)
    s.add_argument('--registry')
    s.add_argument('--output')
    s.set_defaults(func=cmd_plan)
    s=sub.add_parser('selftest')
    s.set_defaults(func=cmd_selftest)
    a=p.parse_args(argv)
    return a.func(a) or 0

if __name__=='__main__':
    raise SystemExit(main())
