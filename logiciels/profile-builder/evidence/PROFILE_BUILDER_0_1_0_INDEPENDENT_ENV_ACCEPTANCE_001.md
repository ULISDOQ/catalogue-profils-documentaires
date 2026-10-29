# Profile Builder 0.1.0 — independent environment acceptance evidence

**Subject:** PROFILE_BUILDER_0_1_0_INDEPENDENT_ENV_ACCEPTANCE_001  
**Environment identity:** intentionally not recorded  
**Python:** 3.12.3 observed  
**Status:** PASS

## Reproducible characteristics

```text
os_family=Linux
profile_builder_version=0.1.0
ged_core_machine_version=0.1.0-candidate
ruleset_version=0.1.0
capability_registry_version=0.1.0-candidate
network_required=false
llm_required=false
external_python_dependency_required=false
system_service_mutation_required=false
```

## Self-test

```text
ged03_replay=PASS
unknown_fail_closed=PASS
overall=PASS
deterministic_replay_sha256=f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

## GED-03 deterministic plan

Selected:

1. `NATIVE_MIME_EMAIL_EXTRACTION_V0.1`
2. `JSON_SCHEMA_VALIDATION`

Excluded:

- `PROFILE_DRIVEN_OCR_GEOMETRIC_EXTRACTION_V0.1`
- `ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC`
- `LLM`

Canonical plan SHA-256:

```text
f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

Serialized output SHA-256 observed:

```text
38a30b3eaff1c23f88f2c40c610b32817c02cc57574d50da4b9663b1837e3dff
```

The exact host name, local account and filesystem path are deliberately excluded because they are irrelevant to reproducibility and belong to the tester's private environment.

## Acceptance

```text
PACKAGE_DISTRIBUTION=PASS
INDEPENDENT_LINUX_RUNTIME_COMPATIBILITY=PASS
GED03_DETERMINISTIC_REPLAY=PASS
UNKNOWN_FAIL_CLOSED=PASS
```
