# GED_CORE_MACHINE_CONTRACT_V0_1

**Référence :** GED-CORE-MACHINE-CONTRACT-001
**Statut :** candidat exécutable de contrat machine — chantier Profile Builder

## 1. Objet

Ce contrat définit le noyau machine-readable minimal permettant à ULISDOQ Profile Builder de transformer un corpus documentaire caractérisé et un besoin explicite en un plan de traitement déterministe et, lorsque les capacités disponibles le permettent, en un package de profil candidat.

Le contrat ne qualifie pas la production. Il formalise la fabrication reproductible d'un candidat.

## 2. Invariant déterministe

```text
same CHARACTERIZATION
+ same REQUESTED_NEED
+ same GED_CORE_MACHINE_VERSION
+ same CAPABILITY_REGISTRY_VERSION
+ same RULESET_VERSION
=
same PLANNING_DECISION
+ same PROCESSING_PLAN
```

Les implémentations doivent canoniser les entrées avant décision et ne doivent pas dépendre d'un ordre non déterministe, d'une date implicite, d'un service externe non versionné ou d'une génération probabiliste.

## 3. Entrées

### 3.1 CHARACTERIZATION

Description factuelle du document/corpus avant choix du traitement.

Doit pouvoir exprimer au minimum :

- type de conteneur et extension ;
- structure native disponible ou non ;
- texte natif disponible ou non ;
- présence d'image/rendu ;
- pagination ;
- statut du corpus ;
- contraintes locales de confidentialité ;
- propriétés observées utiles au routage.

### 3.2 REQUESTED_NEED

Décrit ce que le contributeur veut obtenir, sans imposer la technique.

Exemples : reconnaître une famille documentaire, extraire des champs, produire un JSON normalisé, contrôler des règles métier.

### 3.3 CAPABILITY_REGISTRY

Registre versionné des capacités connues de GED-core Machine.

Chaque capacité déclare :

- identifiant/version ;
- fonction ;
- préconditions ;
- types d'entrées ;
- types de sorties ;
- dépendances ;
- coût qualitatif ;
- contraintes ;
- statut de maturité ;
- preuves disponibles ;
- adaptateur exécutable éventuel.

## 4. Sortie de planification

Le moteur produit toujours une décision explicite parmi :

```text
PROFILE_CANDIDATE_PRODUCED
NO_EXTRA_PROCESSING_REQUIRED
REUSE_PROFILE
ADAPT_PROFILE
COMPOSE_CAPABILITIES
SPECIALIZATION_REQUIRED
CAPABILITY_GAP
AMBIGUOUS
UNSUPPORTED
INSUFFICIENT_CORPUS
```

Une absence de capacité suffisante ne doit jamais être masquée par une invention implicite.

## 5. Règles v0.1

### R1 — réemploi exact

Si un profil existant satisfait exactement la caractérisation et le besoin demandé, préférer `REUSE_PROFILE`.

### R2 — structure native

Si le document possède une structure native et qu'une capacité native couvre entièrement le besoin demandé, exclure OCR et reconnaissance visuelle du plan.

### R3 — minimum suffisant

Parmi plusieurs plans satisfaisant toutes les exigences, choisir celui dont le coût ordonné est minimal.

Ordre de coût v0.1, du moins coûteux au plus coûteux :

```text
NATIVE_PARSE
RULE_BASED_PARSE
TEXT_MATCHER
STRUCTURAL_MATCHER
OCR
VISUAL_MATCHER
SPECIALIZED_ENGINE
LEARNED_MODEL
EXTERNAL_ESCALATION
```

Cet ordre est une convention de planification v0.1, pas une vérité universelle. Il doit être versionné et pourra évoluer.

### R4 — spécialisation avant invention

Si aucune capacité existante ne couvre entièrement le besoin mais qu'une capacité voisine est déclarée adaptable, produire `ADAPT_PROFILE` ou `SPECIALIZATION_REQUIRED` selon le contrat de cette capacité.

### R5 — plafond explicite

Si le registre ne contient aucune composition capable de satisfaire le besoin, produire `CAPABILITY_GAP` ou `UNSUPPORTED`.

### R6 — exclusions justifiées

Le processing plan doit lister les capacités explicitement non retenues lorsqu'elles auraient pu être envisagées, avec une raison déterministe.

## 6. Processing plan

Le plan doit contenir :

- versions du moteur, règles et registre ;
- décision ;
- capacités sélectionnées, dans leur ordre d'exécution ;
- capacités exclues et motifs ;
- profil réutilisé/adapté le cas échéant ;
- préconditions non satisfaites ;
- résultat attendu ;
- limites ;
- empreinte canonique du plan.

## 7. Candidate profile package

Lorsqu'un profil candidat peut être produit, le package doit référencer :

- identité/version du profil ;
- famille documentaire ;
- reconnaissance ;
- extraction ;
- schéma de sortie ;
- bindings/configuration ;
- capacités et versions employées ;
- plan déterministe source ;
- corpus et empreintes ;
- protocole de test ;
- preuves ;
- limites et dettes ;
- statut de qualification.

Le statut initial est toujours `CANDIDATE_UNQUALIFIED` sauf décision de qualification distincte.

## 8. Non-objectifs v0.1

- aucune génération libre de code ;
- aucun LLM dans le chemin déterministe ;
- aucune dépendance réseau nécessaire à la planification ;
- aucune promotion automatique en production ;
- aucune prétention à couvrir tous les formats.

## 9. Compatibilité Profile Builder

Le CLI futur doit être une enveloppe du moteur et de ces contrats. Il ne doit pas dupliquer les règles de planification dans l'interface.

## 10. Premier test de conformité

GED-03 doit pouvoir être rejoué rétrospectivement :

```text
message/rfc822 + native_structure=true
+ need=structured_message_extraction
→ select NATIVE_MIME_EMAIL_EXTRACTION_V0.1
→ exclude OCR
→ exclude VISUAL_MATCHER
→ exclude LLM
→ processing plan deterministic
```

Ce replay est un test de contrat, pas une nouvelle qualification de GED-03.