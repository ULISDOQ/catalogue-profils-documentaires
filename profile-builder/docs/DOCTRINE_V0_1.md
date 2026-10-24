# ULISDOQ Profile Builder — Doctrine v0.1

**Référence :** PROFILE-BUILDER-DOCTRINE-0.1
**Version :** 0.1.0
**Statut :** doctrine candidate en vigueur pour GED-04

## 1. Objet

Cette doctrine définit le cadre de fabrication, de revue et de promulgation des profils documentaires candidats produits avec ULISDOQ Profile Builder.

Elle vise simultanément :

- l'accélération de la phase 1 ;
- la reproductibilité de la fabrication ;
- la protection des documents et valeurs privés ;
- la séparation entre contribution candidate et profil disponible ;
- le maintien de l'autorité humaine aux points où une responsabilité réelle existe.

## 2. Principe général

```text
besoin documentaire réel
→ traitement local autorisé
→ caractérisation
→ GED-core Machine
→ profil candidat
→ privacy/publication gate
→ quarantaine
→ revue probante
→ décision d'autorité
→ promulgation éventuelle
→ silo ouvert
```

## 3. Déterminisme

Pour une même version de :

- GED-core Machine ;
- capability registry ;
- ruleset ;
- entrées caractérisées ;
- besoin demandé ;

le plan de traitement doit être reproductible.

```text
same inputs
+ same machine versions
=
same planning decision
+ same processing plan
```

## 4. Le plus peut le moins

Le Profile Builder mobilise le minimum suffisant parmi les capacités connues.

Il ne doit pas exécuter automatiquement toutes les capacités disponibles.

```text
REUSE_BEFORE_SPECIALIZE
SPECIALIZE_BEFORE_INVENT
GENERALIZE_FROM_EVIDENCE
USE_MINIMUM_SUFFICIENT_CAPABILITIES
```

## 5. Plafond explicite

Le Builder est plafonné par l'état publié de GED-core Machine et du capability set.

```text
PROFILE_BUILDER_vX
<= GED_CORE_MACHINE_vX
<= CAPABILITY_SET_vX
```

Lorsqu'une capacité manque, les sorties normales incluent :

- `CAPABILITY_GAP` ;
- `SPECIALIZATION_REQUIRED` ;
- `AMBIGUOUS` ;
- `UNSUPPORTED` ;
- `INSUFFICIENT_CORPUS`.

Ces sorties ne constituent pas des échecs de méthode.

## 6. Séparation privé / public

```text
LOCAL_PRIVATE_WORKSPACE
!=
PUBLIC_EXPORT_PACKAGE
```

Le workspace privé peut contenir les documents réels et les valeurs observées.

Le package public est reconstruit par allowlist.

Les valeurs observées, sources brutes, OCR brut, chemins locaux, ground truth privés et logs contenant des données documentaires sont non exportables par défaut.

## 7. Champ ≠ valeur

Le Builder doit distinguer structurellement :

```text
FIELD_DEFINITION
!=
OBSERVED_VALUE
```

Une définition de champ peut être publiée ; une valeur réelle observée dans un document ne l'est pas.

## 8. Privacy/publication gate

Avant toute sortie candidate publique :

```text
ALLOWLIST_PATHS=PASS
NO_RAW_SOURCE_FILES=PASS
NO_OBSERVED_VALUES=PASS
NO_LOCAL_PATHS=PASS
SYNTHETIC_FIXTURES_ONLY=PASS
CANARY_NON_LEAKAGE_TEST=PASS
MANUAL_REVIEW_REQUIRED=YES
```

Le gate automatique réduit le risque mais ne remplace pas l'autorité humaine.

## 9. Canary test

Une valeur canari privée et unique est injectée dans le workspace privé.

Le package exportable doit contenir :

```text
CANARY_OCCURRENCES=0
```

Le test canari démontre la non-fuite du canari sur le chemin testé ; il ne constitue pas seul une preuve absolue d'absence de toute donnée personnelle.

## 10. Quarantaine

Un profil candidat ayant franchi le privacy gate n'est pas automatiquement disponible dans ULISDOQ.

Il entre dans une zone dédiée :

```text
CANDIDATE_SUBMITTED
→ PENDING_PROJECT_REVIEW
```

Cette quarantaine est distincte du silo ouvert de profils promulgués.

## 11. Revue probante

La revue questionne le candidat et produit des findings structurés.

```text
OBSERVED
→ CHARACTERIZED
→ EVIDENCED
→ IMPACTED
→ PROPOSED_ACTION
```

Un finding sans preuve reste une hypothèse de revue.

Les anomalies peuvent porter sur :

- privacy ;
- reconnaissance ;
- extraction ;
- sémantique ;
- règles métier ;
- robustesse ;
- reproductibilité ;
- dépendances ;
- sécurité ;
- licences ;
- documentation ;
- généralisation.

## 12. Rôle d'un reviewer assisté

Un fil ChatGPT ou autre assistant peut :

- questionner ;
- rechercher des contradictions ;
- proposer des tests ;
- caractériser des anomalies ;
- relier des preuves ;
- produire une synthèse ;
- vérifier une correction.

Il ne possède pas automatiquement l'autorité de promulgation.

## 13. Autorité humaine

Deux actes restent humains :

### Autorité source

Autoriser l'utilisation locale du corpus.

### Autorité de promulgation

Décider si le candidat peut devenir un profil disponible dans le silo ouvert.

```text
AUTOMATIC_GATE_PASS
!=
HUMAN_AUTHORIZATION
```

## 14. États du candidat

Cycle candidat :

```text
CANDIDATE_UNQUALIFIED
→ PUBLICATION_GATE_PASS
→ CANDIDATE_SUBMITTED
→ PENDING_PROJECT_REVIEW
→ ACCEPTED | CORRECTIONS_REQUIRED | REJECTED
```

Si `ACCEPTED` :

```text
ACCEPTED
→ PUBLISHED
→ OPEN_PROFILE_STORE
```

## 15. Invariants

```text
PUBLIC_CANDIDATE != PUBLISHED_PROFILE
PRIVACY_PASS != QUALITY_PASS
AUTOMATIC_GATE_PASS != HUMAN_AUTHORIZATION
REVIEW_RESULT != PROMULGATION
```

## 16. Rôle des phases

### Phase 1

Explorer largement et fabriquer rapidement des profils candidats reproductibles.

### Phase 2

Qualifier, consolider, généraliser et traiter les dettes observées.

### Phase 3

Promouvoir uniquement les profils et capacités suffisamment qualifiés pour la production.

## 17. Application à GED-04

GED-04 est le premier cas prospectif traité sous cette doctrine versionnée.

Le Profile Builder et GED-core Machine ne doivent pas être modifiés avant le premier résultat de planification GED-04, sauf correction d'un défaut indépendant du cas.

Les résultats `CAPABILITY_GAP`, `SPECIALIZATION_REQUIRED`, `AMBIGUOUS`, `UNSUPPORTED` ou `INSUFFICIENT_CORPUS` restent des résultats valides.

## 18. Références

- `specs/GED_CORE_MACHINE_CONTRACT_V0_1.md` ;
- `specs/PUBLICATION_BOUNDARY_V0_1.md` ;
- `docs/CANDIDATE_LIFECYCLE.md` ;
- `docs/CANDIDATE_REVIEW.md` ;
- `schemas/candidate_review_finding_v0_1.schema.json`.

## 19. Versioning

Toute modification de cette doctrine doit :

- augmenter sa version ;
- expliciter le delta ;
- préciser l'impact sur les Profile Builder déjà distribués ;
- ne pas réécrire rétroactivement les preuves d'un GED-N.

## 20. Décision

```text
DOCTRINE_VERSION=0.1.0
IN_FORCE_FOR=GED-04
STATUS=CANDIDATE_NORMATIVE
```