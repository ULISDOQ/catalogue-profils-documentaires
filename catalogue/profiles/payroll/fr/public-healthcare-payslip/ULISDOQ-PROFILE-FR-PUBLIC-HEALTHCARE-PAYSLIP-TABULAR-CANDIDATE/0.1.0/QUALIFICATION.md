# GED-05 — Qualification protocol for the payslip profile candidate

## Objective

Qualify the documentary profile by replaying it over several monthly payslips from the same real lineage.

The local runtime is not asked to rediscover the document semantics. Its primary job is to test whether the instructed profile remains valid over time.

## Three independent questions

1. **Recognition** — does the document satisfy the candidate documentary signature?
2. **Extraction** — can the declared fields be recovered with correct column/section semantics?
3. **Invariant/variation model** — do predicted invariants remain stable and predicted variables vary without breaking the profile?

## Per-document result

For every field:

```text
field_id
status = VALUE | EMPTY | NOT_APPLICABLE | UNKNOWN | ERROR
source_page
source_region_or_anchor
extraction_method
comparison_to_private_ground_truth = PASS | FAIL | NOT_CHECKED
```

Private observed values remain local.

## Corpus-level measures

- recognition pass / reject / unknown;
- mandatory-field recovery rate;
- optional-field recovery rate;
- table-row reconstruction accuracy;
- employee/employer column separation errors;
- false value rate;
- explicit UNKNOWN rate;
- invariant survival rate;
- expected variation observed;
- unexpected layout drift;
- case-specific manual reinterpretation count.

## Qualification failure signal

If each new month requires changing the generic profile grammar or moving anchors manually, the current profile abstraction is too brittle.

If new months are handled mostly by the same grammar while values and conditional rows vary, the invariant model is supported.

## Promotion boundary

This candidate remains `CANDIDATE_UNQUALIFIED` until the multi-month replay is complete.

A same-employee monthly corpus can qualify template stability, but does not alone prove generality across all employees or payroll issuers.
