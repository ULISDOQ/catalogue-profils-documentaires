# GED-core Machine & ULISDOQ Profile Builder — candidat architectural v0.1

**Référence :** GED-CORE-MACHINE-PROFILE-BUILDER-ARCH-001
**Statut :** candidat architectural capitalisé ; application non encore implémentée

## 1. Intention

ULISDOQ doit pouvoir distribuer un outil permettant à un contributeur de fabriquer localement un nouveau profil documentaire candidat pour un type de document nouveau, sans devoir connaître l'architecture interne du projet.

La cible sépare deux objets :

- **GED-core Machine** : moteur déterministe, versionné, machine-readable, qui décrit et applique les règles de caractérisation, de réemploi, de composition, de spécialisation, de planification, d'évaluation et de capitalisation ;
- **ULISDOQ Profile Builder** : application distribuable qui utilise GED-core Machine pour construire un profil documentaire candidat à partir d'un corpus autorisé et d'un besoin documentaire.

## 2. Principe directeur

```text
GED_CORE_MACHINE_vX
+ CAPABILITY_SET_vX
+ INPUT_DOCUMENTS
+ REQUESTED_NEED
=
DETERMINISTIC_PROCESSING_PLAN
+ CANDIDATE_PROFILE_PACKAGE
+ TESTS
+ EVIDENCE
+ LIMITS
+ DEBT
```

Pour une même version de GED-core Machine, un même registre de capacités et les mêmes entrées, la décision produite doit être reproductible.

```text
same inputs
+ same GED_CORE_MACHINE version
+ same capability registry
=
same decision
+ same processing plan
+ same candidate package
```

## 3. Le plafond de la boîte à outils

Le Profile Builder est volontairement plafonné par le meilleur état connu et publié de GED-core Machine et de son registre de capacités.

```text
PROFILE_BUILDER_vX
<= GED_CORE_MACHINE_vX
<= CAPABILITY_SET_vX
```

Il ne doit pas inventer une capacité absente.

Les sorties normales incluent donc :

- `PROFILE_CANDIDATE_PRODUCED` ;
- `NO_EXTRA_PROCESSING_REQUIRED` ;
- `SPECIALIZATION_REQUIRED` ;
- `CAPABILITY_GAP` ;
- `AMBIGUOUS` ;
- `UNSUPPORTED` ;
- `INSUFFICIENT_CORPUS`.

Un refus explicite est préférable à un profil artificiellement produit.

## 4. Le plus peut le moins

Le fait que GED-core Machine dispose de capacités avancées ne signifie jamais qu'elles doivent toutes être utilisées.

Le plan doit mobiliser le **minimum suffisant**.

Exemples :

```text
EML
→ parsing MIME natif
→ normalisation
→ validation

pas d'OCR
pas de reconnaissance visuelle
pas de LLM
```

```text
formulaire scanné
→ reconnaissance visuelle si nécessaire
→ profil
→ OCR géométrique
→ grammaire métier si nécessaire
```

Principe :

```text
REUSE_BEFORE_SPECIALIZE
SPECIALIZE_BEFORE_INVENT
GENERALIZE_FROM_EVIDENCE
USE_MINIMUM_SUFFICIENT_CAPABILITIES
```

## 5. Objets machine-readable cibles

GED-core Machine devra progressivement formaliser :

1. `characterization` — propriétés observables du document et du corpus ;
2. `requested_need` — informations et niveau de qualité recherchés ;
3. `capability_registry` — capacités disponibles, versions, entrées, sorties, dépendances, coûts, limites et preuves ;
4. `reuse_rules` — règles déterministes de réemploi et d'adaptation ;
5. `processing_plan` — chaîne retenue et capacités explicitement exclues ;
6. `candidate_profile_package` — profil, bindings, contrats, tests et métadonnées ;
7. `assessment` — mesures de qualité, coût, robustesse et réutilisabilité ;
8. `evidence_package` — preuves, empreintes et environnement ;
9. `debt_package` — limites et travaux différés ;
10. `capitalization_decision` — ce qui reste spécifique au profil et ce qui peut enrichir GED-core Machine.

## 6. Deux niveaux de contribution communautaire

### Niveau A — profil réalisable avec la boîte à outils existante

```text
new corpus
→ Profile Builder
→ deterministic plan
→ candidate profile
→ tests
→ evidence package
```

Le contributeur apporte principalement un nouveau corpus autorisé, une configuration et éventuellement des bindings.

### Niveau B — plafond atteint

```text
Profile Builder
→ CAPABILITY_GAP / SPECIALIZATION_REQUIRED
→ proposition d'une nouvelle primitive
→ revue
→ tests
→ éventuelle intégration dans GED-core Machine
→ nouvelle version du capability set
```

Une nouvelle primitive n'est promue que si sa réutilisabilité est démontrée.

## 7. Rôle dans les phases ULISDOQ

### Phase 1 — diversité et accélération

Le Profile Builder doit réduire le coût marginal de création des GED-N et rendre les contributions extérieures praticables.

### Phase 2 — qualité et qualification

La matière produite en phase 1 permet de regrouper les primitives, éliminer les doublons, renforcer les matchers, enrichir les grammaires métier et conduire des tests indépendants.

### Phase 3 — production

Les profils et capacités suffisamment qualifiés peuvent être épinglés, exécutés localement, contrôlés et mis à jour selon une politique explicite.

Le Profile Builder produit des **candidats** ; il ne qualifie pas automatiquement la production.

## 8. Métadonnées minimales d'une contribution

Une contribution produite par le Builder doit pouvoir déclarer :

```text
BUILDER_VERSION
GED_CORE_MACHINE_VERSION
CAPABILITY_SET_VERSION
INPUT_CORPUS_IDENTITY
REQUESTED_NEED
PROCESSING_PLAN
PROFILE_ID
PROFILE_VERSION
PROFILE_SHA256
TEST_PROTOCOL
EVIDENCE
LIMITS
DEBTS
QUALIFICATION_STATUS
```

## 9. Frontières de sécurité et confidentialité

- aucun document privé n'est transmis automatiquement à ULISDOQ ;
- le traitement nominal est local ;
- les pièces jointes et contenus actifs ne sont jamais exécutés par défaut ;
- les preuves publiées doivent être minimisées et vérifiées ;
- les profils candidats ne sont jamais promus automatiquement ;
- les versions des capacités et dépendances sont explicites.

## 10. Cible applicative

Le premier produit distribuable visé est un **Profile Builder CLI minimal**, puis éventuellement une interface plus accessible.

Le CLI devra rester une enveloppe du moteur déterministe, et non contenir une logique métier parallèle.

Architecture cible :

```text
ULISDOQ Profile Builder
        ↓
GED-core Machine
        ↓
Capability Registry
        ↓
Deterministic Planner
        ↓
Adapters / Matchers / Parsers / OCR / Validators
        ↓
Candidate Profile Package
        ↓
Tests + Evidence + Debt
```

## 11. Prochaine étape

Créer un chantier distinct de production de l'application Profile Builder.

Premiers objets attendus :

- `GED_CORE_MACHINE_CONTRACT_V0_1` ;
- schéma de caractérisation ;
- registre minimal des capacités ;
- schéma de processing plan ;
- règles déterministes v0.1 ;
- schéma de candidate profile package ;
- CLI minimal ;
- test rétrospectif GED-03 ;
- premier test prospectif sur un GED-N nouveau.

## 12. Décision

```text
ARCHITECTURE_CANDIDATE=ACCEPTED_FOR_CAPITALIZATION
PROFILE_BUILDER=TARGET_DISTRIBUTABLE_APPLICATION
IMPLEMENTATION=SEPARATE_FUTURE_WORK_ITEM
PRODUCTION_QUALIFICATION=NO
```