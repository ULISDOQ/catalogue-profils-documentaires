from __future__ import annotations
import hashlib, json
from copy import deepcopy
MACHINE_VERSION='0.1.0-candidate'
RULESET_VERSION='0.1.0'

def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def _sha(obj):
    return hashlib.sha256(_canon(obj).encode('utf-8')).hexdigest()

def _preconditions_satisfied(cap, characterization):
    nf=characterization.get('native_features', {})
    obs=characterization.get('observations', {})
    available={
        'native_structure': bool(nf.get('structured')),
        'text_available': bool(nf.get('text_available')),
        'image_available': bool(nf.get('image_available')),
        **{k:v for k,v in obs.items() if isinstance(v,(bool,int,float,str))}
    }
    for key, expected in (cap.get('preconditions') or {}).items():
        if key == 'schema_available':
            continue
        if available.get(key) != expected:
            return False
    return True

def _container_match(cap, characterization):
    c=characterization.get('container', {})
    media=(c.get('media_type') or '').casefold()
    ext=(c.get('extension') or '').casefold()
    inputs={str(x).casefold() for x in cap.get('inputs', [])}
    return bool(media and media in inputs) or bool(ext and ext in inputs)

def plan(characterization, requested_need, registry):
    required=list(requested_need.get('required_outputs') or [])
    caps=sorted(
        registry.get('capabilities', []),
        key=lambda c:(int(c.get('cost_rank',10**9)), c.get('capability_id',''), c.get('version',''))
    )
    native=[
        c for c in caps
        if c.get('class') == 'NATIVE_PARSE'
        and c.get('deterministic', False)
        and _container_match(c, characterization)
        and _preconditions_satisfied(c, characterization)
        and set(required).issubset(set(c.get('outputs', [])))
    ]
    selected=[]
    excluded=[]
    limits=[]
    unsatisfied=[]
    decision='CAPABILITY_GAP'
    if native:
        p=native[0]
        selected.append({
            'capability_id':p['capability_id'],
            'version':p['version'],
            'order':1,
            'reason':'Native structured container satisfies requested extraction without OCR or visual recognition'
        })
        limits.extend(p.get('limits', []))
        v=next((c for c in caps if c.get('capability_id') == 'JSON_SCHEMA_VALIDATION'), None)
        if v:
            selected.append({
                'capability_id':v['capability_id'],
                'version':v['version'],
                'order':2,
                'reason':'Validate normalized deterministic output'
            })
        excluded=[
            {'capability_id':'PROFILE_DRIVEN_OCR_GEOMETRIC_EXTRACTION_V0.1','reason':'Native text and MIME structure already satisfy the need'},
            {'capability_id':'ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC','reason':'Visual recognition is unnecessary for container-native identity'},
            {'capability_id':'LLM','reason':'Not required and not part of deterministic capability set'}
        ]
        decision='PROFILE_CANDIDATE_PRODUCED'
    else:
        unsatisfied=required[:] or ['NO_REQUIRED_OUTPUT_DECLARED']
    out={
        'schema_version':'ged-core-processing-plan/0.1',
        'ged_core_machine_version':MACHINE_VERSION,
        'ruleset_version':RULESET_VERSION,
        'capability_registry_version':registry.get('registry_version','UNKNOWN'),
        'decision':decision,
        'selected_capabilities':selected,
        'excluded_capabilities':excluded,
        'reused_profile_id':None,
        'unsatisfied_requirements':unsatisfied,
        'expected_outputs':required,
        'limits':limits,
        'canonical_sha256':None
    }
    h=deepcopy(out)
    h['canonical_sha256']=None
    out['canonical_sha256']=_sha(h)
    return out
