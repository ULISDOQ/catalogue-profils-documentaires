# Profile Builder — frontière de publication publique v0.1

**Référence :** PROFILE-BUILDER-PUBLICATION-BOUNDARY-001
**Statut :** exigence bloquante avant GED-04 prospectif

## 1. Problème

Le dépôt ULISDOQ communautaire est public. Une erreur de confusion entre **nom de champ** et **valeur observée dans un document réel** pourrait publier une donnée personnelle ou confidentielle.

Une simple consigne « ne pas publier de données personnelles » n'est pas une preuve suffisante.

## 2. Invariant

```text
LOCAL_PRIVATE_WORKSPACE
!= PUBLIC_EXPORT_PACKAGE
```

Le Profile Builder ne doit jamais transformer implicitement son espace de travail local en contenu publiable.

Le package public est construit **à partir d'une allowlist de classes d'artefacts**, et non par copie du workspace.

## 3. Données autorisées dans un export public

Peuvent être exportés, après validation :

- identifiants techniques de profil et de capacités ;
- noms de champs génériques ;
- types et schémas de données ;
- coordonnées géométriques normalisées ne contenant aucune valeur documentaire ;
- règles de transformation et de validation génériques ;
- versions, hashes, paramètres et dépendances ;
- résultats agrégés/minimisés ;
- statuts, limites et dettes formulés sans valeurs sources ;
- fixtures synthétiques explicitement marquées comme telles.

## 4. Données interdites par défaut

Ne doivent jamais être exportés automatiquement :

- contenu brut d'un document réel ;
- valeur extraite d'un document réel ;
- texte OCR brut ;
- corps de courriel réel ;
- nom, prénom, adresse, téléphone, e-mail, identifiant administratif, bancaire ou médical observé ;
- chemin local contenant une identité ;
- nom de fichier réel non explicitement autorisé ;
- captures, images ou extraits réels ;
- ground truth dérivé d'un document personnel ;
- logs contenant des valeurs documentaires.

## 5. Séparation champ / valeur

Le Builder doit distinguer structurellement :

```text
FIELD_DEFINITION
  name
  type
  semantic_role
  extraction_rule

OBSERVED_VALUE
  value
  source
  confidence
```

`OBSERVED_VALUE` appartient au workspace privé et est **non exportable par défaut**.

Un profil public peut contenir `field_name="postal_address"`, mais jamais la valeur réelle observée dans le document source.

## 6. Construction de l'export

L'export public doit être produit dans un répertoire neuf :

```text
PRIVATE_WORKSPACE/
    corpus/
    raw_outputs/
    local_ground_truth/
    local_logs/

PUBLIC_EXPORT_STAGING/
    profile/
    schemas/
    rules/
    tests_synthetic/
    evidence_minimized/
    manifest.json
```

Aucun `cp -r` du workspace vers l'export n'est autorisé.

## 7. Gate déterministe

Avant qu'un package soit déclaré `PUBLIC_EXPORT_READY`, il doit satisfaire simultanément :

```text
ALLOWLIST_PATHS=PASS
NO_RAW_SOURCE_FILES=PASS
NO_OBSERVED_VALUES=PASS
NO_LOCAL_PATHS=PASS
SYNTHETIC_FIXTURES_ONLY=PASS
CANARY_NON_LEAKAGE_TEST=PASS
MANUAL_REVIEW_REQUIRED=YES
```

Le gate automatique ne remplace pas la revue humaine ; il réduit le risque d'erreur.

## 8. Test canari obligatoire

Le test de non-fuite doit injecter dans le workspace privé une valeur canari unique, par exemple :

```text
ULISDOQ_PRIVATE_CANARY_<random-unique-id>
```

Le Builder exécute le même chemin de fabrication puis construit le package public.

Le gate vérifie que le canari n'apparaît dans **aucun octet** du package exportable.

Le test doit porter sur :

- profil ;
- schémas ;
- règles ;
- tests ;
- preuves ;
- manifest ;
- archive finale.

Résultat requis :

```text
CANARY_OCCURRENCES=0
```

## 9. Limite de la preuve

Un test canari démontre l'absence de fuite du canari sur le chemin testé. Il ne prouve pas mathématiquement l'absence de toute donnée personnelle.

La garantie recherchée repose donc sur plusieurs couches :

1. séparation architecturale privé/public ;
2. export par allowlist ;
3. schémas interdisant les valeurs observées ;
4. scanners de motifs à risque ;
5. test canari ;
6. revue humaine avant publication.

## 10. Git

Le Profile Builder ne doit pas effectuer lui-même de `git add`, `git commit` ou `git push` vers le dépôt public dans sa version initiale.

Il produit un package de staging. La publication est une action distincte, explicite et révisée.

## 11. Décision

```text
PUBLIC_REPOSITORY_DATA_LEAK_PREVENTION=REQUIRED
GED04_PROFILE_BUILD_PUBLIC_EXPORT=BLOCKED_UNTIL_GATE_IMPLEMENTED
PROFILE_BUILDER_0_1_0=PLANNING_ONLY_ACCEPTED
NEXT_PROFILE_BUILDER_VERSION=ADD_PUBLICATION_GATE
```