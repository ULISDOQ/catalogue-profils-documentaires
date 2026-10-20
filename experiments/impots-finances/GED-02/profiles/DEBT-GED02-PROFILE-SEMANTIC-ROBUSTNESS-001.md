# DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001

**Status:** OPEN — non-blocking for phase 1  
**Profile:** `ULISDOQ-PROFILE-FR-2044-CANDIDATE`  
**Deferral target:** profile qualification / phase 2

## Observation

The profile-driven S11 scan extraction demonstrates that the GED-02 profile is already technically useful for local 2044 recognition and structured extraction, but semantic robustness is not yet sufficient for qualification.

Observed phase-1 result:

```text
FISCAL_CORE_ARITHMETIC=PASS
PROFILE_BINDING=PARTIAL
TEXT_SEMANTICS=PARTIAL
STATUS_SEMANTICS=PARTIAL
OVERALL=PARTIAL_STRONG
```

## Explicit debt

1. **Computed-field consistency.**  
   DGFIP business rules should detect OCR drift on calculated fields. Example: line 420 was read as `591` while the fiscal chain implies `5910`.

2. **Binding refinement for property metadata.**  
   `property_1.rental_units` was read as `4` for a scenario containing one rented local.

3. **Text semantic validation.**  
   A value such as `|` must not be accepted as a valid postal address. It should become `UNREADABLE` or `AMBIGUOUS`.

4. **Status semantics.**  
   `VALUE=0`, `EMPTY` and `NOT_APPLICABLE` must remain distinguishable where DGFIP semantics require it.

## Phase-1 decision

```text
DO_NOT_PERFECT_NOW
PROFILE_QUALIFICATION=NOT_YET
PRODUCTION_QUALIFICATION=NO
GED02_PHASE1_CONTINUATION=COMPLETE_ENOUGH
NEXT=GED-N+1
```

This debt does not invalidate the phase-1 experiment. It records what must be revisited before claiming a locally qualified 2044 profile.
