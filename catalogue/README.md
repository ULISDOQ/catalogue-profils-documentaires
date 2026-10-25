# ULISDOQ Catalogue

This directory is the canonical documentary-knowledge surface.

It is distinct from:
- `experiments/`: historical evidence, exploratory work and research debt;
- `profile-builder/`: generic profile-building/planning tooling;
- `ULISTAG/`: recognition implementations;
- `client/`: executable adapters.

## Organizing principle

The catalogue is organized by documentary category, not by experiment number, employer, software vendor, or current implementation.

```text
catalogue/
  index.json
  profiles/
    <domain>/
      <jurisdiction>/
        <documentary-category>/
          <profile-id>/
            <version>/
              profile.json
              grammar.json
              QUALIFICATION.md
              EVIDENCE.md
```

## Category identity rule

A category profile contains the smallest identity statement that defines the documentary category.

Everything else belongs to one of:
- semantic grammar;
- extraction grammar;
- observed variation;
- optional specialization/adapters;
- qualification evidence.

For GED-05:

```text
CATEGORY = BULLETIN_DE_PAIE_FRANCAIS
CATEGORY_INVARIANT = DOCUMENT_IS_A_FRENCH_PAYSLIP
```

Employer identity, employee identity, payroll software, exact layout, coordinates, labels and payroll codes are not category invariants.

## Promotion boundary

`CANDIDATE_UNQUALIFIED` profiles may exist in the catalogue for study and replay.

A profile is not automatically selectable merely because it exists in `catalogue/`.

Qualification and publication remain distinct.
