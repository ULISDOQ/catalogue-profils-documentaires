# Factures & achats — famille documentaire

Cette famille regroupe les expériences ULISDOQ consacrées aux **factures, achats, reçus et documents fournisseurs**, indépendamment d'un fournisseur, d'un moteur ou d'un modèle particulier.

## Objet

Les expériences de cette famille servent à éprouver le cycle commun :

```text
document local
→ reconnaissance du modèle documentaire
→ TAG / empreinte structurelle
→ profil d'extraction candidat
→ moteur compatible
→ extraction
→ contrôles
→ qualification bornée
```

Un profil de facture n'est pas qualifié par sa seule présence dans le dépôt. Sa qualification doit préciser le modèle documentaire couvert, les versions, le moteur utilisé, le corpus d'épreuve, les contrôles, les limites et les preuves.

Les documents privés de production restent chez le consommateur. ULISDOQ publie des fixtures autorisées, profils, TAGs, protocoles et résultats qui peuvent l'être.

## Organisation

Chaque sous-dossier `GED-NN/` est une expérience bornée portant sur un cas de facture particulier. Il contient ses propres fixtures, profils ou templates, tests et preuves.

Le client générique ULISDOQ reste dans [`/client`](../../client/README.md) : une expérience utilise le client mais n'en est pas propriétaire.

## Expériences

- [GED-01 — Fournisseur-EXP-01](GED-01/README.md) : première expérience de profil de facture et de rapprochement avec une source réelle conservée localement.

D'autres expériences de factures pourront être ajoutées ici sans modifier le contrat général de la famille.
