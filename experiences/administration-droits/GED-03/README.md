# GED-03 — Dossier de préparation phase 1

**Référence : GED03_PHASE1_PREPARATION_AUTHORIZED_001**  
**État courant : phase 1 exécutée sur corpus synthétique, candidat non qualifié pour la production.**

Résultats et limites : [RESULTS_V0_1.md](RESULTS_V0_1.md).

Le dossier de préparation historique ci-dessous est conservé pour la filiation ; ses mentions de travaux futurs et de non-exécution décrivent la préparation initiale, pas l’état courant.

## Objet

Éprouver, lors d'une future exécution distinctement autorisée, la formule :

```text
GED-core + Nouveau_document_N -> GED-N
```

sur une famille documentaire structurée n'appelant a priori ni OCR ni reconnaissance visuelle : le courriel `.eml`.

## Corpus synthétique

Positifs :

- `corpus/S01_SIMPLE_TEXT.eml`
- `corpus/S02_MULTIPART_ALT.eml`
- `corpus/S03_ATTACHMENT_PDF.eml`
- `corpus/S04_MULTI_RECIPIENTS.eml`
- `corpus/S05_ENCODED_FOLDED_HEADERS.eml`
- `corpus/S06_UNICODE_ATTACHMENT.eml`

Négatifs / limites :

- `corpus/N01_RENAMED_TEXT.eml`
- `corpus/N02_MALFORMED_MIME.eml`
- `corpus/N03_TRUNCATED.eml`

Oracle séparé :

- `corpus/GROUND_TRUTH_V0_1.json`

Toutes les adresses utilisent `.test`. Le corpus ne contient aucun courriel personnel.

## Contrats

- `contrats/normalized_eml_schema_v0_1.json` : contrat JSON normalisé ;
- `REUSE_MATRIX_V0_1.md` : réemploi / non-réemploi proposé ;
- `PHASE1_PROTOCOL_V0_1.md` : protocole futur d'exécution ;
- `MEASURES_V0_1.json` : critères de mesure de la fabrique ;
- `TECHNICAL_DELTAS_V0_1.md` : développements manquants identifiés ;
- `EXECUTION_AUTHORIZATION_REQUEST_001.txt` : saisine de GED-RÉEL.

## Chaîne cible

```text
EML local
→ parseur MIME Python stdlib email
→ normalisation ULISDOQ
→ validation du schéma
→ freeze
→ comparaison au ground truth
```

## Traitements explicitement absents

```text
OCR=NO
VISUAL_MATCHER=NO
LLM=NO
NETWORK=NO
ATTACHMENT_EXECUTION=NO
```

Ces absences sont une partie du test GED-core : la fabrique doit savoir ne pas mobiliser une capacité inutile.

## Deltas avant exécution — préparation historique

Deux deltas principaux sont identifiés, mais non implémentés :

1. adaptateur local `EmailMessage -> normalized EML JSON` ;
2. évolution générique du registre pour permettre une reconnaissance `CONTAINER_NATIVE` sans imposer un TAG ULISTAG visuel.

Aucune dépendance Python externe n'est attendue pour le premier essai : la bibliothèque standard `email` doit être évaluée en premier.

## Frontière de la préparation initiale — historique

```text
CORPUS=READY
CONTRACT=READY
GROUND_TRUTH=READY
REUSE_MATRIX=READY
PROTOCOL=READY
MEASURES=READY
TECHNICAL_DELTAS=IDENTIFIED

IMPLEMENTATION=NOT_AUTHORIZED_BY_PREPARATION_ORDER
EXECUTION=NOT_PERFORMED
PCIA_DEPLOYMENT=NO
RUNTIME_MUTATION=NO
```
