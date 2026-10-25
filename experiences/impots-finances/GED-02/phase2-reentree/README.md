# GED-02 — package de reprise phase 2

## État laissé par la phase 1

GED-02 est clos pour la poursuite horizontale avec un résultat `PHASE1_CONCLUSIVE`.

La phase 1 a démontré :

```text
2044 candidate recognition
→ explicit profile discovery
→ profile loading
→ versioned geometric binding
→ local OCR by bound ROI
→ semantic JSON
→ DGFIP business-coherence review
```

Le profil reste volontairement **candidat non qualifié**. La dette connue n'est pas un échec de phase 1 : elle constitue le point de reprise de phase 2.

## Point de reprise obligatoire

Commencer par :

`../profils/DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001.md`

Puis relire :

- `SOURCE_MANIFEST_V0_1.json`
- `preuves/S11_PROFILE_DRIVEN_EXTRACTED_FROZEN.json`
- `preuves/S11_DGFIP_SYNTHETIC_GROUND_TRUTH.json`
- `../profils/fr_formulaire_2044_candidate.json`
- `../extraction/fr_2044_2025_property1_binding_v0_1.json`
- `../extraction/semantic_extraction_schema_v0_1.json`
- `../../../../client/profile_ocr_extract_v0_1.py`
- `../../../../project/PROFILE_REGISTRY_V0_1.json`

## Résultat métier conservé

Le cœur fiscal extrait est cohérent sur :

```text
215 = 211+212+213+214
240 = sum(221..229)-230
261 = 215-240-250
263 = 261+262
```

La reprise phase 2 doit traiter explicitement les écarts suivants sans les masquer :

```text
420 OCR drift:
  observed 591
  expected/business-consistent 5910

property_1.rental_units:
  observed 4
  scenario expected 1

property_1.address:
  observed "|"
  incorrectly classified VALUE

semantic statuses:
  VALUE=0 / EMPTY / NOT_APPLICABLE not yet robustly distinguished
```

## Objet de la phase 2

La phase 2 n'a pas à redémontrer la chaîne de bout en bout depuis zéro.

Elle doit partir de l'implémentation existante et traiter les deltas de qualification :

1. règles de cohérence métier pour champs calculés ;
2. validation sémantique des champs texte ;
3. raffinement ciblé des bindings fautifs ;
4. sémantique des statuts ;
5. mesures indépendantes de robustesse sur variantes et négatifs ;
6. qualification explicite du profil local 2044 si les preuves deviennent suffisantes.

## Frontière de preuve

Le ground truth est un oracle d'évaluation, jamais une source de génération ou de correction de l'extraction.

La référence officielle vierge et les spécimens synthétiques binaires sont identifiés par SHA-256 dans le manifest. Ne jamais remplacer un binaire absent par un fichier seulement ressemblant.

## Confidentialité

Le package de reprise ne contient aucune donnée fiscale personnelle. Les identités et adresses présentes dans le ground truth sont synthétiques et explicitement fictives.

## Décision de phase 1

```text
PROFILE_QUALIFICATION=NOT_YET
PRODUCTION_QUALIFICATION=NO
LOCAL_2044_QUALIFICATION=ENVISAGEABLE
DEBT=OPEN_NON_BLOCKING
NEXT_PHASE1=GED-N+1
PHASE2_REENTRY=READY
```
