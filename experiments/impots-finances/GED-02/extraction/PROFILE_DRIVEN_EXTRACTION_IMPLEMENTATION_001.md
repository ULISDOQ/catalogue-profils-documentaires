# PROFILE_DRIVEN_OCR_GEOMETRIC_EXTRACTION — implementation check 001

**Subject:** `GED02_S11_PROFILE_DRIVEN_EXTRACTION_IMPLEMENTATION_001`  
**Status:** local implementation evidence; not PCIA acceptance evidence.

## Implemented objects

- `project/PROFILE_REGISTRY_V0_1.json`
- `client/profile_ocr_extract_v0_1.py`
- `client/deployment/profile_ocr_extract_manifest_v0_1.json`
- `experiments/impots-finances/GED-02/profiles/fr_formulaire_2044_candidate.json` v0.3.0
- `experiments/impots-finances/GED-02/extraction/fr_2044_2025_property1_binding_v0_1.json`
- `deployment/ubuntu/complete-v0_1/requirements-profile_extraction.txt`

## Binding provenance

Official blank source:

```text
filename=2044_5132.pdf
sha256=6c9798559408deef0646cf93cbf9f933c7da1cbd404ac2129e54d52fc3369e9b
pages=4
```

The 25 field bindings were measured from the official blank form only.

No S11 ground-truth file was read or used while constructing the binding.

Scope:

- official fiscal lines 211..263 selected for S11;
- official line 420;
- property_1 tenant;
- property_1 address;
- property_1 rental_units.

## Local controls

```text
python syntax=PASS
binding JSON parse=PASS
profile discovery=PASS
profile loading=PASS
binding loading=PASS
semantic schema validation=PASS
traceability hashes emitted=PASS
ground_truth_access=NONE
```

### Official blank-form control

The adapter was run against the official blank 2044.

Result:

```text
FIELDS=25
VALUE=0
UNREADABLE=25
INVENTED_VALUE=0
```

This conservative result is expected for the blank control in v0.1: the candidate does not yet infer EMPTY solely from absence of OCR text.

### Synthetic S11 source control — before scan degradation

The adapter was also run locally on the synthetic S11 source PDF, not on the PCIA gray scan, and without ground-truth access.

Result:

```text
FIELDS=25
VALUE=23
UNREADABLE=2
SCHEMA_VALIDATION=PASS
GROUND_TRUTH_ACCESS=NONE
```

The two unreadable fields were the free-text property tenant and property address regions.

This is useful implementation evidence that the profile-driven ROI path functions, but it does **not** qualify the method on the scanned S11 specimen.

## Remaining qualification

The next valid experiment is one controlled PCIA Gate B run against:

`GED02-S11_2044_2025_SYNTHETIC_COMPLETE_SCAN_GRAY.pdf`

with:

1. Gate A evidence already fixed;
2. exact registry/profile/binding identities recorded;
3. extraction frozen before ground-truth access;
4. semantic schema validation;
5. separate field-level comparison after freeze.

No full PCIA reinstall is required. Only the missing profile-extraction runtime delta may be installed if absent.
