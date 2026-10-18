# ULISDOQ — Unificateur documentaire libre

**Unificateur Libre Interprofessionnel de Sources Documentaires Qualifiées**

*Explorer les documents. Partager les connaissances. Qualifier l'information.*

ULISDOQ est un **unificateur libre de ressources et de capacités documentaires** : il référence, relie, versionne et qualifie les sources, formats, profils, moteurs et contrôles nécessaires au traitement informationnel local. Il ne se substitue pas aux moteurs techniques.

[Lire le prologue fondateur](PROLOGUE_FONDATEUR.md).

## Périmètre

Le référentiel relie sélectivement des profils, sources, méthodes et briques techniques utiles à la reconnaissance, la classification, l'extraction et la validation des documents : factures, documents administratifs et officiels, documents de santé et autres familles pertinentes. Il ne prétend pas référencer tout Internet.

Les briques techniques sont des ressources parmi N, caractérisées par leurs capacités, interfaces, versions, licences, compatibilités, limites et preuves. Les noms d'outils particuliers sont réservés à leurs fiches techniques ou aux expériences unitaires. Voir [l'architecture d'unification](project/UNIFICATION_TECHNICAL_COMPONENTS.md).

## Horizontalité et identités canoniques

**[HORIZON-IDENTITY-001 — Référentiel canonique et correspondances](project/HORIZON_IDENTITY_MAPPING.md)** : dissocier entités, formats et profils ; concevoir un référentiel extensible d'entités sans fixer de nombre cible ; « 88 821 » n'est qu'un exemple arbitraire, équivalent à « des milliers de fournisseurs référencés ». Les noms commerciaux n'appartiennent pas aux identifiants de profils.

## Qualification

Une source identifiée n'est pas nécessairement un profil d'extraction qualifié. Un profil qualifié sur un périmètre donné ne garantit pas tous les résultats d'extraction. Chaque proposition devra préciser provenance, droits, version, critères de reconnaissance, contrôles et limites.

## Horizon déclaré : reconnaître automatiquement les formats

**[HORIZON-FORMAT-001 — Architecture conceptuelle du « Shazam documentaire »](project/HORIZON_FORMAT_MATCHER.md)** : établir, sur des corpus indépendants, des TAGs de formats qualifiés permettant aux clients de retrouver le profil d'extraction adapté. Horizon de recherche et de qualification, **non une fonctionnalité déjà opérationnelle**. Priorité au réemploi des mécanismes existants.

## Expériences par familles documentaires

La famille [Factures](experiments/factures/README.md) regroupe les expériences de profils de factures. [GED-01](experiments/factures/GED-01/README.md) en est le premier cas borné.

## Démonstration de classification locale

Le [protocole TAG candidat](project/TAG_CANDIDATE_PROTOCOL.md) fournit un éditeur local minimal et expose la prochaine fonction manquante : la consultation du catalogue. Le cas [GED-02 — formulaire 2044](experiments/formulaires/GED-02/README.md) examine la généralité du modèle hors factures ; il reste non qualifié.

## Participer

Consulter [CONTRIBUTING.md](CONTRIBUTING.md). Les contributions sont soumises à revue avant intégration. **Aucun document personnel réel, donnée médicale identifiable, secret ou document confidentiel ne doit être déposé ici.**

## Statut

**Amorçage public.** Les profils candidats, licences de contenu et règles définitives de gouvernance restent en qualification. Aucun profil d'extraction n'est annoncé comme validé à ce stade.
