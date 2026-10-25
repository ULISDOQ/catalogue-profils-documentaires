# GED-05 — Bulletin de paie français

## Purpose

GED-05 is the catalogue-first qualification experiment for the documentary category:

```text
BULLETIN_DE_PAIE_FRANCAIS
```

The canonical profile is NOT duplicated in `experiments/`.

Canonical profile:

```text
catalogue/profiles/payroll/fr/bulletin-de-paie-francais/
ULISDOQ-PROFILE-FR-BULLETIN-DE-PAIE-CANDIDATE/
0.1.0/
```

## Experiment role

This directory contains:
- GED-05 experiment framing;
- corpus/evidence references;
- qualification results;
- reuse/RETEX material.

It does not own the documentary profile.

## Current specimens

- Specimen A: real French payslip, March 2025, private source.
- Specimen B: real French payslip, December 2024, different employer and materially different layout, private source.

Private source files and private observed values are not committed here.

## Current objective

Test whether the same documentary category and grammar remain valid across:
- different employers;
- different layouts;
- multiple months;
- changing payroll rows and values.

## Boundary

```text
experiments/payroll/GED-05/
= experiment + evidence

catalogue/.../ULISDOQ-PROFILE-FR-BULLETIN-DE-PAIE-CANDIDATE/
= canonical reusable documentary knowledge
```
