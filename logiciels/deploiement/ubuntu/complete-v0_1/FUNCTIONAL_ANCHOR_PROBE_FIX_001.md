# COMPLETE_PROFILE_FUNCTIONAL_ANCHOR_PROBE_FIX_001

**Scope:** correction ciblée de la probe `functional_anchor_graph` uniquement.  
**PCIA execution:** NO.

## Correction

Dans `logiciels/deploiement/ubuntu/complete-v0_1/verify_complete.py`, l'ancre synthétique `NUMBER` attendait :

```text
FACTURE N TEST 001 DU 01 01 2026
```

alors que `pdfplumber.extract_words()` retourne notamment :

```text
FACTURE
N
TEST-001
DU
01/01/2026
```

et que `phrase_box()` normalise chaque mot sans aplatir ensuite les sous-tokens issus de la ponctuation.

La probe utilise désormais l'ancre stable :

```text
FACTURE N
```

Aucun changement de l'algorithme `anchor_graph` n'a été effectué.

## Probe locale ciblée

Fixture PDF identique au test global :

```text
ULISDOQ FACTURE TEST
FACTURE N TEST-001 DU 01/01/2026
Montant facture (EUR) 42,00
```

Observation avec la logique `norm()+phrase_box()` de `ulistag_v0.py` :

```text
TITLE_FOUND=YES
NUMBER_FOUND_WITH_FIXED_ANCHOR=YES
OLD_NUMBER_ANCHOR_FOUND=NO
RESULT=PASS
```

La correction porte uniquement sur la donnée synthétique de vérification et ne change ni méthode, ni seuil, ni comportement ULISTAG en production.

## Commit

`567bb01c712ef1753a9300cb6f110e700139cfb2`
