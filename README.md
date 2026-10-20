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

## Faisabilité de couverture documentaire

Une première [étude de dimensionnement](project/ETUDE_FAISABILITE_COUVERTURE_PROFILS_1000_ORGANISATIONS.md) examine l'ordre de grandeur du nombre de profils qualifiés nécessaire pour viser environ 80 % de la paperasserie courante de 1 000 organisations. L'hypothèse centrale est d'environ 1 000 profils, à vérifier sur un corpus représentatif ; l'indicateur principal est le **taux de documents couverts**, non le nombre brut de profils.

## Qualification

Une source identifiée n'est pas nécessairement un profil d'extraction qualifié. Un profil qualifié sur un périmètre donné ne garantit pas tous les résultats d'extraction. Chaque proposition devra préciser provenance, droits, version, critères de reconnaissance, contrôles et limites.

## Horizon déclaré : reconnaître automatiquement les formats

**[HORIZON-FORMAT-001 — Reconnaissance et qualification des formats documentaires](project/HORIZON_FORMAT_MATCHER.md)** : établir, sur des corpus indépendants, des TAGs de formats qualifiés permettant aux clients de retrouver le profil d'extraction adapté. Horizon de recherche et de qualification, **non une fonctionnalité déjà opérationnelle**. Priorité au réemploi des mécanismes existants.

## ULISTAG — reconnaissance documentaire

[ULISTAG](ULISTAG/README.md) est le sous-système cœur d'ULISDOQ consacré à la description, l'indexation et la reconnaissance structurelle des modèles documentaires.

Son cycle de conception est séparé pour préserver la lisibilité d'ULISDOQ. Les méthodes génériques vivent dans `ULISTAG/` ; leur élaboration et leurs preuves spécifiques restent dans les répertoires `experiments/.../GED-N/ulistag/`.

La [roadmap ULISTAG](ULISTAG/ROADMAP.md) vise une première phase d'environ 70 types, formats et fournisseurs différents afin de faire émerger empiriquement les primitives, regroupements et matchers réellement réutilisables.

## Expériences par familles documentaires

Pour rendre le catalogue immédiatement lisible, les premières expériences sont rangées dans six familles documentaires courantes :

- [Factures & achats](experiments/factures/README.md)
- [Impôts & finances](experiments/impots-finances/README.md)
- [Santé & protection sociale](experiments/sante-protection-sociale/README.md)
- [Assurances & sinistres](experiments/assurances/README.md)
- [Administration & droits](experiments/administration-droits/README.md)
- [Logement, véhicules & services courants](experiments/logement-vehicules-services/README.md)

Ces familles constituent un classement humain de haut niveau ; elles ne remplacent ni les TAGs de format, ni les profils techniques.

[GED-01](experiments/factures/GED-01/README.md) est le premier cas borné de la famille Factures. [GED-02 — formulaire 2044](experiments/impots-finances/GED-02/README.md) éprouve surtout le lien entre un document administratif et la connaissance officielle publiée qui lui est associée.

## Démonstration de classification locale

Le [protocole TAG candidat](project/TAG_CANDIDATE_PROTOCOL.md) fournit un éditeur local minimal et expose la prochaine fonction manquante : la consultation du catalogue.

## Participer

Consulter [CONTRIBUTING.md](CONTRIBUTING.md). Les contributions sont soumises à revue avant intégration. **Aucun document personnel réel, donnée médicale identifiable, secret ou document confidentiel ne doit être déposé ici.**

## Statut

**Amorçage public.** Les profils candidats, licences de contenu et règles définitives de gouvernance restent en qualification. Aucun profil d'extraction n'est annoncé comme validé à ce stade.
