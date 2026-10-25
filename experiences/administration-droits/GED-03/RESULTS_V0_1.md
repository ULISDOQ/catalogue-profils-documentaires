# GED-03 — Phase 1 bounded implementation and test RETEX

Subject: GED03_PHASE1_BOUNDED_IMPLEMENTATION_AND_TEST_001

## Result

POSITIVES=6/6 PASS
NEGATIVES_OR_LIMITS=3/3 EXPLICITLY FLAGGED
SCHEMA_VALIDATION=9/9 PASS
GROUND_TRUTH_COMPARISON=9/9 PASS
OCR_CALLS=0
VISUAL_MATCHER_CALLS=0
LLM_CALLS=0
NETWORK_CALLS_IN_CODE_PATH=0
ATTACHMENT_EXECUTION=0
NEW_EXTERNAL_PYTHON_DEPENDENCIES=0
PROFILE_QUALIFICATION=NONE
PRODUCTION_QUALIFICATION=NO

Observed statuses:
S01 PARSED
S02 PARSED
S03 PARSED
S04 PARSED
S05 PARSED
S06 PARSED
N01 INVALID
N02 MALFORMED
N03 TRUNCATED

## Adaptive-factory finding

GED-03 supports the GED-core hypothesis on this bounded corpus:
structured container -> native parser -> normalized contract -> schema validation -> freeze -> evaluation.

The useful adaptation was mainly the removal of unnecessary processing. No OCR, visual matcher, invoice extractor, LLM or network service was needed.

## Reusable additions

- generic CONTAINER_NATIVE recognition mode in the profile registry;
- generic container-native resolver;
- local stdlib-email normalization adapter pattern;
- GED-core measurement object;
- explicit post-freeze ground-truth comparison pattern.

## Environment note

The test used local isolated Python execution with python -I. Kernel-level network namespace isolation was unavailable. The executed adapter contains no network operation in its code path and records network_used=false; this is not a kernel proof that networking was impossible.

## Debt

See DEBT-GED03-STRUCTURAL-VALIDATION-DIVERSITY-001.md.

## Decision

GED-03 is strongly conclusive for phase 1 within the synthetic corpus. It demonstrates that GED-core can select a much simpler chain than GED-02 while preserving contracts and evidence.

This does not qualify all EML files or the profile for production.