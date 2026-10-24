# GED-01 → GED-04 — reusable bricks for GED-05

**Status:** candidate consolidation after GED-04 profile construction.

The objective is not to maximize reuse. It is to make each new GED start from known, independently selectable bricks and add only the missing delta.

| Brick | Origin | GED-04 use | GED-05 default posture |
|---|---|---|---|
| Text anchors + normalized geometry | GED-01 | candidate structural recognition / field localization | REUSE if stable anchors exist |
| Recognition separated from extraction | GED-02 | recognition can remain unqualified while extraction grammar is instructed | REUSE |
| Profile-driven geometric extraction | GED-02 | targeted rendered-region fallback candidate | REUSE/ADAPT only when needed |
| Visual keypoint matcher | GED-02 | deliberately not required for initial GED-04 extraction | OPTIONAL, evidence-driven |
| Native/container-first processing | GED-03 | reinforces cheapest sufficient path | REUSE |
| Explicit UNKNOWN / malformed states | GED-03 | no silent invention for unreadable fields | REUSE |
| JSON schema validation | GED-01/02/03 | output-structure validation | REUSE |
| Provenance/version/evidence separation | GED-01/02/03 | candidate package and qualification boundaries | REUSE |
| Consumer escalation protocol | GED-04 | unknown profile -> governed documentary instruction | REUSE for any consumer |
| Documentary instruction -> profile candidate | GED-04 | semantic model and grammar materialized without private source publication | REUSE |
| Native-text + targeted render fallback | GED-04 | handles partially degraded PDF text without full OCR | REUSE/ADAPT |

## Expected GED-05 starting algorithm

```text
CHARACTERIZE SOURCE
→ SEARCH EXISTING PROFILE / FAMILY
→ SELECT MINIMUM SUFFICIENT CAPABILITY
→ if known: EXTRACT + VALIDATE
→ if unknown: CONSUMER ESCALATION
→ DOCUMENTARY INSTRUCTION
→ REUSE / SPECIALIZE / NEW CANDIDATE
```

GED-05 should therefore start with a reuse matrix before any new component is proposed.

A new component is justified only when the requested outcome cannot be satisfied by composition or specialization of registered bricks.
