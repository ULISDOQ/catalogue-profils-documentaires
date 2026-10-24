# ULISDOQ Profile Builder 0.1.1 — matcher-selection candidate

**Status:** TARGETED_TESTS_PASS / SOURCE_PINNED

## Identity

```text
PROFILE_BUILDER_VERSION=0.1.1
GED_CORE_MACHINE_VERSION=0.1.0-candidate
RULESET_VERSION=0.1.0
MATCHER_SELECTION_POLICY_VERSION=0.1.1
SOURCE_COMMIT=a05e61d3240d0f29aec45251e5340c1c41513275
```

## Scope

0.1.1 adds deterministic selection of existing registered matchers for requested outputs when their declared preconditions are satisfied.

It does **not** execute matchers.

It contains no GED-04-specific selection rule.

## Cost policy

Eligible matchers are ordered by declared `cost_rank`.

- a unique lowest cost is selected;
- a higher-cost eligible matcher is excluded with an explicit reason;
- equal lowest costs produce `AMBIGUOUS` with no arbitrary selection.

The policy is versioned as `0.1.1`.

## Result semantics

The existing processing-plan schema is intentionally preserved for compatibility with current consumers.

For a matcher-selection success, `PROFILE_CANDIDATE_PRODUCED` remains the legacy-compatible decision value, but the plan adds:

```text
PLANNING_ONLY_PROFILE_NOT_MATERIALIZED
```

to `limits`.

Therefore:

```text
PROFILE_CANDIDATE_PRODUCED in a processing plan
!=
materialized candidate profile package
```

This semantic debt remains explicit until a future contract version can rename the planning success state without breaking existing consumers.

## Targeted qualification

```text
T1 GED-03 exact regression + canonical hash: PASS
T2 anchor-graph only eligible: PASS
T3 visual-keypoints only eligible: PASS
T4 both eligible, lowest cost wins: PASS
T5 equal lowest cost -> AMBIGUOUS, no arbitrary choice: PASS
T6 neither eligible -> CAPABILITY_GAP: PASS
T7 deterministic replay + no matcher runtime dependency: PASS

TARGETED_TESTS=7/7 PASS
GED03_CANONICAL_SHA256=f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

## Direct source-tree entrypoint

From the `profile-builder/` directory:

```bash
python3 -m ulisdoq_profile_builder info
python3 -m ulisdoq_profile_builder selftest
python3 -m ulisdoq_profile_builder plan \
  --characterization <characterization.json> \
  --need <requested_need.json> \
  --output <processing_plan.json>
```

No network, matcher execution, private export or profile promulgation is performed by the planner.
