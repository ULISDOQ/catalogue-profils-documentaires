from __future__ import annotations
import hashlib, json
from copy import deepcopy

MACHINE_VERSION='0.1.0-candidate'
RULESET_VERSION='0.1.0'
MATCHER_SELECTION_POLICY_VERSION='0.1.1'
MATCHER_CLASSES={'STRUCTURAL_MATCHER','VISUAL_MATCHER'}

def _canon(obj):
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':'))

def _sha(obj):
    return hashlib.sha256(_canon(obj).encode('utf-8')).hexdigest()

def _available_preconditions(characterization):
    nf=characterization.get('native_features', {})
    obs=characterization.get('observations', {})
    return {
        'native_structure': bool(nf.get('structured')),
        'text_available': bool(nf.get('text_available')),
        'image_available': bool(nf.get('image_available')),
        **{k:v for k,v in obs.items() if isinstance(v,(bool,int,float,str))}
    }

def _unmet_preconditions(cap, characterization):
    available=_available_preconditions(characterization)
    unmet=[]
    for key, expected in (cap.get('preconditions') or {}).items():
        if key == 'schema_available':
            continue
        if available.get(key) != expected:
            unmet.append((key, expected, available.get(key)))
    return unmet

def _preconditions_satisfied(cap, characterization):
    return not _unmet_preconditions(cap, characterization)

def _container_match(cap, characterization):
    c=characterization.get('container', {})
    media=(c.get('media_type') or '').casefold()
    ext=(c.get('extension') or '').casefold()
    inputs={str(x).casefold() for x in cap.get('inputs', [])}
    return bool(media and media in inputs) or bool(ext and ext in inputs)

def _matcher_reason(cap):
    return (
        'Registered deterministic matcher satisfies requested output and declared '
        f'preconditions; selected by matcher policy {MATCHER_SELECTION_POLICY_VERSION} '
        f'at cost_rank={int(cap.get("cost_rank",10**9))}'
    )

def _matcher_exclusion_reason(cap, characterization, selected_cost=None):
    unmet=_unmet_preconditions(cap, characterization)
    if unmet:
        details=', '.join(
            f'{key} expected {expected!r} observed {observed!r}'
            for key, expected, observed in unmet
        )
        return f'Declared preconditions not satisfied: {details}'
    if selected_cost is not None:
        cost=int(cap.get('cost_rank',10**9))
        if cost > selected_cost:
            return (
                f'Eligible matcher not selected because cost_rank={cost} is higher '
                f'than selected cost_rank={selected_cost}'
            )
    return 'Eligible matcher not selected'

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
        matcher_candidates=[
            c for c in caps
            if c.get('class') in MATCHER_CLASSES
            and c.get('deterministic', False)
            and set(required).issubset(set(c.get('outputs', [])))
        ]
        eligible=[
            c for c in matcher_candidates
            if _preconditions_satisfied(c, characterization)
        ]
        if eligible:
            lowest_cost=int(eligible[0].get('cost_rank',10**9))
            lowest=[
                c for c in eligible
                if int(c.get('cost_rank',10**9)) == lowest_cost
            ]
            if len(lowest) == 1:
                p=lowest[0]
                selected.append({
                    'capability_id':p['capability_id'],
                    'version':p['version'],
                    'order':1,
                    'reason':_matcher_reason(p)
                })
                limits.extend(p.get('limits', []))
                limits.append('PLANNING_ONLY_PROFILE_NOT_MATERIALIZED')
                excluded=[
                    {
                        'capability_id':c['capability_id'],
                        'reason':_matcher_exclusion_reason(c, characterization, lowest_cost)
                    }
                    for c in matcher_candidates
                    if c.get('capability_id') != p.get('capability_id')
                ]
                decision='PROFILE_CANDIDATE_PRODUCED'
            else:
                tied_ids=sorted(c.get('capability_id','') for c in lowest)
                excluded=[
                    {
                        'capability_id':c['capability_id'],
                        'reason':(
                            f'Equal lowest cost_rank={lowest_cost}; deterministic policy '
                            'forbids arbitrary tie-breaking'
                        )
                    }
                    for c in lowest
                ]
                limits.append(
                    'AMBIGUOUS_EQUAL_COST_MATCHERS:' + ','.join(tied_ids)
                )
                unsatisfied=required[:] or ['NO_REQUIRED_OUTPUT_DECLARED']
                decision='AMBIGUOUS'
        else:
            excluded=[
                {
                    'capability_id':c['capability_id'],
                    'reason':_matcher_exclusion_reason(c, characterization)
                }
                for c in matcher_candidates
            ]
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
