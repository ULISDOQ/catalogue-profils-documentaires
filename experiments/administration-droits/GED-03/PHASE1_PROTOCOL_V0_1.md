# GED-03 — Protocole proposé de phase 1

**Référence : GED03-PHASE1-PROTOCOL-001**  
**Statut : PREPARED_NOT_EXECUTED**

## Préconditions

- corpus uniquement synthétique ;
- aucune connexion réseau requise ;
- aucune ouverture/exécution des pièces jointes ;
- aucune mutation PCIA ;
- bibliothèque standard Python `email` évaluée avant toute dépendance externe.

## Étape A — caractérisation

Pour chaque spécimen, relever sans interprétation de contenu :

- présence d'en-têtes RFC ;
- structure MIME ;
- multipart ou non ;
- types de parties ;
- présence de pièces jointes ;
- charset/encodage ;
- anomalies de structure.

Décision attendue : `NATIVE_PARSE_CANDIDATE` ou `INVALID/AMBIGUOUS`.

## Étape B — plan GED-core

Produire un plan explicite :

```text
recognition=CONTAINER_NATIVE
ocr=NO
visual_matcher=NO
llm=NO
network=NO
parser=python_stdlib_email_candidate
normalization=GED03_OUTPUT_CONTRACT_V0_1
```

Si ce plan n'est pas suffisant, retourner le delta observé au lieu d'ajouter silencieusement une dépendance.

## Étape C — extraction candidate

Lors d'une future exécution autorisée :

1. lire les octets localement ;
2. parser avec la politique moderne de la bibliothèque Python `email` ;
3. normaliser les en-têtes sans inventer les absents ;
4. sélectionner le corps texte selon une règle documentée ;
5. inventorier les pièces jointes sans les exécuter ;
6. produire le JSON conforme au schéma ;
7. inclure source SHA-256 et identité du parseur ;
8. geler le résultat.

## Étape D — négatifs

N01 ne doit pas devenir `PARSED` uniquement parce que l'extension vaut `.eml`.

N02 et N03 doivent exposer l'anomalie. Si la bibliothèque standard tolère la structure, les défauts/defects retournés par le parseur doivent être examinés et traduits en statut explicite ; aucune tolérance silencieuse n'est qualifiée.

## Étape E — comparaison

Seulement après freeze :

- comparer champs attendus ;
- comparer statut attendu ;
- vérifier les noms Unicode ;
- vérifier destinataires multiples ;
- vérifier multipart alternative ;
- vérifier inventaire des pièces jointes.

## Critères de passage phase 1

```text
C1_CHARACTERIZATION=PASS
C2_PROPORTIONAL_PLAN=PASS
C3_VALID_POSITIVES=6/6 or explicit bounded defect
C4_NEGATIVES_NOT_SILENTLY_ACCEPTED=3/3
C5_SCHEMA_VALIDATION=PASS
C6_OCR_CALLS=0
C7_VISUAL_MATCHER_CALLS=0
C8_LLM_CALLS=0
C9_NETWORK_CALLS=0
C10_REUSE_MEASURES_RECORDED=PASS
```

Un défaut borné peut produire `PARTIAL` sans bloquer le passage au GED suivant.
