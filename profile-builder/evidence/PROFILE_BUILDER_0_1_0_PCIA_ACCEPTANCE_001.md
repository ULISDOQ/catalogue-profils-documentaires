# Profile Builder 0.1.0 — PCIA acceptance

**Subject:** PROFILE_BUILDER_0_1_0_PCIA_ACCEPTANCE_001
**Host:** PC-13333330
**Execution root:** /home/utilisateur/ULISDOQ/ulisdoq-profile-builder-0.1.0
**Python:** 3.12.3
**Status:** PASS

## Observed package identity

```text
profile_builder_version=0.1.0
ged_core_machine_version=0.1.0-candidate
ruleset_version=0.1.0
capability_registry_version=0.1.0-candidate
network_required=false
llm_required=false
```

## Self-test

```text
ged03_replay=PASS
unknown_fail_closed=PASS
overall=PASS
deterministic_replay_sha256=f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

## GED-03 deterministic plan

Decision:

```text
PROFILE_CANDIDATE_PRODUCED
```

Selected:

1. NATIVE_MIME_EMAIL_EXTRACTION_V0.1
2. JSON_SCHEMA_VALIDATION

Excluded:

- PROFILE_DRIVEN_OCR_GEOMETRIC_EXTRACTION_V0.1
- ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC
- LLM

Observed canonical plan SHA-256:

```text
f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

Serialized `/tmp/ged03-plan.json` SHA-256:

```text
38a30b3eaff1c23f88f2c40c610b32817c02cc57574d50da4b9663b1837e3dff
```

The serialized-file hash and canonical-plan hash are different objects and are not expected to be equal.

## Acceptance

```text
PACKAGE_DISTRIBUTION=PASS
PCIA_RUNTIME_COMPATIBILITY=PASS
GED03_DETERMINISTIC_REPLAY=PASS
UNKNOWN_FAIL_CLOSED=PASS
EXTERNAL_PYTHON_DEPENDENCY_REQUIRED=NO_OBSERVED
PCIA_SERVICE_MUTATION=NONE_REPORTED
```

## Consequence

Profile Builder 0.1.0 is accepted as a bounded distributable candidate for the next experiment.

GED-04 must be introduced as a new prospective case. The planner must not be modified in advance to force GED-04 success. `CAPABILITY_GAP` remains an acceptable and informative result.