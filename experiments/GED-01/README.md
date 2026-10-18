# GED-01 — Reconnaissance et extraction de factures

**Statut : CANDIDATE / NOT_RUN.** Première expérience publique ULISDOQ, avec un cas synthétique publiable et une extension prévue à quatre familles de factures issues de documents réels transformés (SFR, électricité, télécommunications, eau).

## Matériaux publics

- `fixtures/facture_fictive_001.txt` : facture fictive textuelle.
- `fixtures/attendu_001.json` : vérité attendue pour cette fixture.
- `profiles/profil_facture_fictive_001.json` : profil candidat.
- `tests/cas_ged01.json` : scénarios positifs/négatifs.
- `docs/PROTOCOLE.md` : protocole d'évaluation.

## SFR-EXP01 : provenance réelle, publication différée

Une facture SFR réelle a été utilisée **hors dépôt** pour créer un dérivé expérimental de deux pages (PNG et PDF image-only) avec substitutions de données personnelles et marquage expérimental. Cette transformation **ne constitue pas une anonymisation certifiée** et ne démontre pas encore la fiabilité d'une extraction.

**Les images, le PDF, l'original, leurs empreintes et les informations permettant de relier ce dérivé à une personne ne sont pas publiés ici** : revue visuelle, risque de réidentification et droits de redistribution de la présentation commerciale restent à instruire.

## Critère de réussite

Une preuve réutilisable requiert : fixture autorisée, valeurs attendues, moteur/version, commande ou procédure reproductible, résultats observés, écarts, contrôles arithmétiques et décision de revue. Aucun profil n'est qualifié à ce jour.
