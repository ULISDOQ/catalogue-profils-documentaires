# ULISTAG — Sous-système de reconnaissance documentaire d'ULISDOQ

ULISTAG est un **sous-système cœur du projet ULISDOQ** consacré à la description, l'indexation et la reconnaissance structurelle des modèles documentaires.

Il possède son propre cycle de conception, d'expérimentation et de qualification, tout en restant intégré au même dépôt et à la même gouvernance générale qu'ULISDOQ.

## Séparation des responsabilités

```text
ULISDOQ
→ projet global, catalogue, profils, client, qualification et architecture générale

ULISTAG/
→ méthodes réutilisables de représentation et reconnaissance documentaire
→ schémas communs
→ matchers génériques
→ protocoles
→ recherche
→ cycle de vie ULISTAG

experiments/.../GED-N/ulistag/
→ application d'ULISTAG à un cas documentaire
→ références spécifiques
→ observations
→ essais
→ paramètres candidats
→ résultats, échecs et RETEX
```

La règle de capitalisation est :

> **GED-N contient la matière expérimentale et les preuves ; ULISTAG contient la méthode réutilisable qui peut en être extraite.**

Les flux fonctionnent dans les deux sens :

```text
GED-N → observation / échec / découverte → ULISTAG cœur
ULISTAG cœur → méthode / matcher / protocole → GED-N → nouvelles preuves
```

## Objectif de phase 1

La phase 1 vise environ **70 types, formats et fournisseurs de documents différents**, y compris des familles encore inconnues aujourd'hui.

Cette diversité doit permettre d'identifier empiriquement :

- quelles primitives documentaires sont réellement réutilisables ;
- quelles familles de matchers émergent ;
- ce qui peut être regroupé ;
- ce qui nécessite une méthode spécialisée ;
- comment réduire efficacement un catalogue potentiellement composé de centaines ou milliers de profils.

ULISTAG ne suppose donc pas qu'un unique mécanisme de TAG saura tout reconnaître.

L'architecture visée est :

```text
DOCUMENT
→ ULISTAG CORE / descripteur minimal
→ index ou pré-sélection rapide
→ petit ensemble de candidats
→ matcher(s) spécialisés
→ modèle(s) documentaire(s) candidat(s)
→ profil(s) associé(s)
```

## Arborescence cœur

- [ROADMAP.md](ROADMAP.md) — cycle de vie et progression ;
- [research/](research/) — état de l'art et travaux de conception génériques ;
- [matchers/](matchers/) — méthodes de comparaison réutilisables ;
- [schemas/](schemas/) — contrats de représentation ;
- [protocols/](protocols/) — protocoles génériques d'évaluation ;
- [tests/](tests/) — tests du cœur, indépendants des preuves propres aux GED-N.

Les données privées ne sont pas capitalisées dans ce dossier.
