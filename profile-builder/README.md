# ULISDOQ Profile Builder

> **Statut actuel : paquet candidat 0.1.0 produit — planner déterministe et CLI disponibles pour acceptation independent Linux test environment ; fabrication automatique d'un nouveau profil pas encore autorisée.**

Le **Profile Builder** est le futur outil distribué avec ULISDOQ pour aider une personne à créer un **profil documentaire candidat** à partir d'un nouveau type de document.

Il est conçu pour être utilisable par un contributeur qui **ne connaît pas l'architecture interne d'ULISDOQ**.

## À quoi servira cet outil ?

Vous disposez par exemple de plusieurs documents du même type :

- un formulaire administratif ;
- une facture ;
- un courriel `.eml` ;
- un relevé ;
- une lettre ;
- un document métier ;
- ou une autre famille documentaire.

Vous voulez permettre à ULISDOQ de reconnaître ce type de document et, si nécessaire, d'en extraire certaines informations de manière locale et reproductible.

Le Profile Builder devra vous guider pour produire un package standard :

```text
vos documents d'essai autorisés
        ↓
Profile Builder
        ↓
caractérisation
        ↓
recherche des capacités déjà disponibles
        ↓
plan de traitement
        ↓
profil candidat
        ↓
tests
        ↓
preuves + limites + dettes
```

## Ce que le Profile Builder ne fera pas

Il ne cherchera pas à « comprendre magiquement » tous les documents.

Il utilisera uniquement les capacités connues de la version installée d'ULISDOQ.

Si le type de document nécessite une capacité absente, l'outil devra le dire clairement, par exemple :

```text
CAPABILITY_GAP
SPECIALIZATION_REQUIRED
UNSUPPORTED
INSUFFICIENT_CORPUS
```

Un profil non produit est parfois un meilleur résultat qu'un mauvais profil.

## Principe : utiliser seulement ce qui est nécessaire

Le Profile Builder pourra connaître de nombreuses techniques : parseurs natifs, OCR, reconnaissance visuelle, extraction géométrique, matchers spécialisés, règles métier, etc.

Mais il ne devra jamais les exécuter toutes par défaut.

Exemple : un courriel `.eml` possède déjà une structure MIME. Il peut souvent être traité directement avec un parseur de courriel, sans OCR ni reconnaissance visuelle.

À l'inverse, un formulaire papier scanné peut nécessiter plusieurs étapes supplémentaires.

Le but est toujours de construire **la chaîne la plus simple qui satisfait le besoin demandé**.

## Vos documents restent locaux

L'objectif d'ULISDOQ est de permettre la construction et l'utilisation des profils sans envoyer automatiquement vos documents privés vers un serveur central.

Le Profile Builder devra donc fonctionner localement par défaut.

Une contribution destinée au catalogue ULISDOQ devra privilégier :

- le profil ;
- les règles ;
- les paramètres ;
- les tests ;
- les résultats minimisés ;
- les empreintes de fichiers ;
- les limites connues ;
- les dettes identifiées.

Ne publiez pas de document personnel, médical, fiscal, confidentiel ou soumis à des droits que vous ne pouvez pas redistribuer.

## Qu'est-ce qu'un profil candidat ?

Un profil candidat décrit comment ULISDOQ peut traiter une famille documentaire donnée.

Selon le cas, il peut contenir ou référencer :

- les critères permettant d'identifier le document ;
- le parseur ou matcher adapté ;
- les champs à extraire ;
- les zones ou règles d'extraction ;
- le schéma du résultat attendu ;
- les contrôles de cohérence ;
- les versions des outils utilisés ;
- les tests réalisés ;
- les limites observées.

**Candidat ne signifie pas qualifié pour la production.**

## Pourquoi les versions sont importantes

Le Profile Builder sera lié à une version précise de la boîte à outils ULISDOQ.

Un package devra donc enregistrer au minimum :

```text
PROFILE_BUILDER_VERSION
GED_CORE_MACHINE_VERSION
CAPABILITY_SET_VERSION
PROFILE_VERSION
```

Cette information permettra de comprendre et de reproduire la manière dont le profil a été fabriqué.

## Comment une contribution pourra évoluer

Deux situations sont prévues.

### 1. ULISDOQ sait déjà traiter ce type de document

Le Builder réutilise et configure les capacités existantes. Le résultat peut devenir une contribution de **nouveau profil**.

### 2. Une capacité manque

Le Builder s'arrête proprement et identifie le manque.

Un développeur ou contributeur avancé pourra alors proposer une nouvelle primitive. Si cette primitive devient suffisamment générique et testée, elle pourra enrichir une future version de GED-core Machine et bénéficier à d'autres profils.

## Pourquoi ce projet est important

ULISDOQ vise à explorer une grande diversité documentaire.

Sans outil de fabrication, chaque nouveau profil demanderait de comprendre le dépôt, les moteurs, les schémas, les tests et les règles internes.

Le Profile Builder doit transformer cela en une démarche guidée, reproductible et plus accessible.

Il doit permettre :

```text
plus de profils candidats en phase 1
        ↓
plus de matière empirique
        ↓
meilleure qualification en phase 2
        ↓
profils réellement exploitables en phase 3
```

## État du chantier

À ce jour :

- l'architecture du Profile Builder est capitalisée ;
- GED-core possède déjà plusieurs capacités expérimentales réutilisables ;
- des profils candidats existent pour plusieurs familles documentaires ;
- un premier mode générique `CONTAINER_NATIVE` a été expérimenté ;
- le contrat machine v0.1 est matérialisé ;
- le capability registry v0.1 est matérialisé ;
- le planner déterministe v0.1 et le CLI minimal sont implémentés ;
- l'acceptation sur un environnement Linux indépendant a été observée PASS.

## Prochain chantier

Le prochain chantier produira progressivement :

1. le contrat machine de GED-core ;
2. le registre des capacités ;
3. les règles de planification déterministes ;
4. le format standard d'un profil candidat ;
5. un CLI minimal ;
6. des tests reproductibles ;
7. un premier profil entièrement fabriqué avec le Builder.

## Pour les futurs contributeurs

Le but n'est pas de vous demander de devenir architecte d'ULISDOQ.

Le but est que vous puissiez apporter un nouveau cas documentaire, comprendre ce que l'outil sait faire ou ne sait pas faire, obtenir des résultats reproductibles et contribuer une matière examinable par le projet.
## Contrat machine v0.1

Le chantier est maintenant entré en production du socle machine-readable.

Les objets initiaux vivent dans :

- `specs/GED_CORE_MACHINE_CONTRACT_V0_1.md` ;
- `schemas/characterization_v0_1.schema.json` ;
- `schemas/requested_need_v0_1.schema.json` ;
- `schemas/capability_registry_v0_1.schema.json` ;
- `schemas/processing_plan_v0_1.schema.json` ;
- `schemas/candidate_profile_package_v0_1.schema.json` ;
- `registry/CAPABILITY_REGISTRY_V0_1.json`.

Un premier replay attendu de GED-03 est préparé sous `examples/ged03/`.

Le planner déterministe v0.1 est maintenant disponible. Le prochain gate est l'acceptation indépendante du paquet 0.1.0 sur independent Linux test environment selon `INDEPENDENT_TEST_ENVIRONMENT_ACCEPTANCE_V0_1.md`, avant toute utilisation prospective sur GED-04.
## Frontière de publication publique

Un document réel et les valeurs observées pendant sa lecture appartiennent au **workspace privé local**.

Le futur package communautaire est un objet différent, reconstruit par allowlist dans un staging neuf. Le Builder ne doit pas publier directement sur Git.

Avant toute contribution issue d'un document réel, un privacy gate devra notamment vérifier l'absence de fichiers sources, valeurs observées, chemins locaux et la non-fuite d'un canari privé.

Référence : `specs/PUBLICATION_BOUNDARY_V0_1.md`.

Le paquet 0.1.0 déjà accepté sur independent Linux test environment reste un paquet de **planification** ; il n'est pas encore autorisé à produire un export public depuis un corpus réel.
## Quarantaine et revue avant publication

Un profil candidat qui a franchi le privacy gate n'est pas encore un profil disponible dans ULISDOQ.

Il entre d'abord en **quarantaine**, avec un statut du type `PENDING_PROJECT_REVIEW`.

Pendant cette phase, il peut être relu, testé, challengé et corrigé. Une anomalie doit être décrite **preuve à l'appui** : résultat de test, fixture synthétique, violation de schéma, comparaison ground truth, hash, contradiction métier, ou autre preuve reproductible.

Le dépôt distingue donc clairement :

```text
PUBLIC_CANDIDATE
!=
PUBLISHED_PROFILE
```

La revue peut être assistée par un fil ChatGPT spécialisé, mais ce fil n'est pas l'autorité de promulgation. Il peut instruire, questionner, proposer des tests et produire des findings structurés.

La promulgation vers le silo ouvert n'intervient qu'après décision explicite de l'autorité du projet.

Documentation :

- `docs/CANDIDATE_LIFECYCLE.md` ;
- `docs/CANDIDATE_REVIEW.md` ;
- `schemas/candidate_review_finding_v0_1.schema.json`.

## Doctrine versionnée

Le chantier applique désormais une doctrine explicite et versionnée.

Référence en vigueur pour GED-04 :

- `docs/DOCTRINE_V0_1.md` ;
- `docs/DOCTRINE_CHANGELOG.md`.

Cette doctrine fixe notamment les règles de déterminisme, confidentialité, quarantaine, revue probante, autorité humaine et promulgation.
