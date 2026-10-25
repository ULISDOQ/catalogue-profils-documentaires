# ULISTAG — Roadmap

**Statut : chantier autonome au sein d'ULISDOQ**

ULISTAG est piloté par ULISDOQ. Les consommateurs externes, dont CLAU/GED-RÉEL, peuvent fournir des cas réels, exécuter des candidats et retourner des preuves, mais ils ne pilotent pas le cycle de conception ULISTAG.

## Phase 1 — diversité documentaire

Cible expérimentale : environ **70 types, formats et fournisseurs différents**.

La phase 1 ne vise pas à créer 70 mécanismes indépendants. Elle vise à découvrir le plus petit ensemble de primitives et de stratégies de comparaison permettant de couvrir cette diversité.

```text
cas documentaires
→ observation
→ primitives candidates
→ regroupements
→ matchers réutilisables
→ indexation / pré-sélection
→ profils candidats
→ tests indépendants
```

## Axes de travail

1. **ULISTAG CORE** — définir un schéma minimal commun : page, primitive, relation, feature, statut, version.
2. **Observation** — rendre interchangeables les lecteurs PDF texte, OCR, image/layout et autres observateurs.
3. **Indexation** — éviter la comparaison exhaustive contre chaque profil ; utiliser des caractéristiques peu coûteuses pour réduire rapidement l'espace de recherche.
4. **Matchers spécialisés** — conserver des méthodes simples et explicables par famille de structure lorsque nécessaire.
5. **Résolution** — lier explicitement un candidat ULISTAG à un ou plusieurs profils documentaires.
6. **Qualification** — positifs, variantes, négatifs proches et corpus indépendants.

## Principe d'évolution

Une méthode spécialisée née dans un GED-N reste dans l'expérience tant qu'elle dépend fortement de ce cas.

Elle est promue dans le cœur `ULISTAG/` lorsqu'elle devient :

- réutilisable sur plusieurs cas ;
- suffisamment séparée des données privées ;
- documentée ;
- testable indépendamment du cas initial.

Les méthodes devenues inutiles peuvent être retirées sans remettre en cause les preuves historiques conservées dans les expériences.

## Dette active GED-01

`DEBT-GED01-ANCHOR-GRAPH-SAME-SUPPLIER-001` — éprouver `ANCHOR_GRAPH_V0_1` sur plusieurs factures distinctes du même fournisseur afin d'en mesurer la stabilité intra-modèle et les limites. Référence : `experiences/factures/GED-01/ulistag/DEBT_SAME_SUPPLIER_VALIDATION.md`.
