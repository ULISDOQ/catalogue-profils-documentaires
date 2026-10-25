# GED-05 — Reuse posture

GED-05 is intentionally catalogue-first.

## Reused without reinvention

- GED-01: textual anchors and geometry as reusable profile primitives.
- GED-02: recognition separate from extraction; geometric/profile binding when needed.
- GED-03: native structure first, minimum sufficient capability, explicit UNKNOWN, schema validation.
- GED-04: source-first documentary instruction, consumer escalation, targeted render fallback.

## New reusable concept introduced by GED-05

```text
PROFILE
=
IDENTITY
+ FIELD SEMANTICS
+ EXTRACTION GRAMMAR
+ INVARIANTS
+ EXPECTED VARIATIONS
+ CONDITIONAL ELEMENTS
+ VERIFICATION RULES
+ QUALIFICATION EVIDENCE
```

The expected gain for GED-06 is that repeated-document families no longer require inventing a new profile model. They should instantiate these primitives and add only the documentary delta.
