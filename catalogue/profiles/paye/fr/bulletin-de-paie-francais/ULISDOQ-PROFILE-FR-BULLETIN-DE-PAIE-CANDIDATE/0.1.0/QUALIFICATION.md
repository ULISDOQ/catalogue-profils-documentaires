# Qualification — Bulletin de paie français

## Category invariant

The only category invariant is:

```text
DOCUMENT_IS_A_FRENCH_PAYSLIP
```

No employer, employee, software, layout or exact field arrangement is part of the category identity.

## GED-05 qualification objective

Test whether the generic grammar can support materially different French payslips without redefining the category or adding employer-specific logic to the parent profile.

## Initial evidence

Two real private specimens are available:

- specimen A: March 2025, public healthcare employer;
- specimen B: December 2024, previous private employer.

They differ substantially in employer, sector, labels, layout and payroll presentation.

## Qualification stages

### Q1 — Cross-employer semantic coverage

For both initial specimens:

- identify the category as French payslip;
- recover pay period;
- recover employer and employee roles;
- recover remuneration structure;
- distinguish employee and employer charges where present;
- recover gross, tax/PAS context and net pay where present;
- preserve monthly/cumulative semantics where present;
- return UNKNOWN instead of guessing.

### Q2 — Multi-month replay

Use several months from at least one lineage to test:
- changing row sets;
- bonuses/allowances/absence lines;
- changing rates/bases/amounts;
- cumulative values;
- layout drift.

### Q3 — Additional layout diversity

Add materially different French payslips until the grammar no longer depends on one issuer/layout.

### Q4 — Negative cases

Include non-payslip payroll/HR documents and foreign payslips/lookalikes.

## Measurements

- correct category / reject / UNKNOWN;
- semantic concept recovery;
- false-value rate;
- UNKNOWN rate;
- employer-specific rule count;
- software-specific rule count;
- manual reinterpretation count;
- grammar changes per new specimen.

## Success signal

The category remains stable while different layouts are processed by the same semantic grammar with only optional extraction adapters.

## Failure signal

If the parent profile accumulates employer names, vendor rules, exact coordinates or per-layout exceptions, the abstraction is wrong.

## Promotion boundary

This profile remains `CANDIDATE_UNQUALIFIED` until cross-employer and multi-month replay evidence is produced.
