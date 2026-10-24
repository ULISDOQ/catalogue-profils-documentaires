# ULISDOQ Profile Builder 0.1.0 — distributable candidate

**Status:** INDEPENDENT_ENVIRONMENT_ACCEPTANCE_PASS

## Identity

```text
PROFILE_BUILDER_VERSION=0.1.0
GED_CORE_MACHINE_VERSION=0.1.0-candidate
RULESET_VERSION=0.1.0
CAPABILITY_REGISTRY_VERSION=0.1.0-candidate
```

## Archive

```text
filename=ulisdoq-profile-builder-0.1.0.tar.gz
sha256=f82e610db48b8d894f702485ec0e7f9fc89599fd385105f19c1b75441fa7a66f
```

## Local validation before distribution

```text
UNIT_TESTS=3/3 PASS
GED03_REPLAY=PASS
UNKNOWN_FAIL_CLOSED=PASS
OVERALL_SELFTEST=PASS
GED03_PROCESSING_PLAN_CANONICAL_SHA256=f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1
```

No external Python package is required by the distributed candidate.

## Scope

This candidate proves the deterministic planning contract and fail-closed behavior. It does **not** yet autonomously characterize GED-04 or fabricate a complete new profile.

After acceptance on an independent Linux test environment, GED-04 may be submitted prospectively to the Builder without modifying the planner to fit the case.
