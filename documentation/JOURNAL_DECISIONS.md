# ULISDOQ — Ledger versionné

Version de structure : **0.1**. Les commits Git constituent l'historique technique ; ce registre porte les décisions et les limites de qualification.

| Date | Référence | Objet | Statut | Preuve / limite |
|---|---|---|---|---|
| 2026-10-18 | IDENTITY-001 | ULISDOQ et lignage ULIS/DOCQ/DOCK | DOCUMENTED | Voir `PROLOGUE_FONDATEUR.md` |
| 2026-10-18 | GED-01 | Première expérience de facture fictive | CANDIDATE | Fixtures et tests définis ; aucune extraction exécutée |
| 2026-10-18 | Fournisseur-EXP-01 | Dérivé expérimental d'une facture Fournisseur-EXP-01 réelle | PRIVATE_REVIEW_REQUIRED | Deux images et PDF image-only préparés hors dépôt ; contrôle confidentialité et droits de publication non achevé |
| 2026-10-18 | GED-01-EXEC | Évaluation du moteur de reconnaissance/extraction | NOT_RUN | Aucune mesure de performance ni qualification revendiquée |

| 2026-10-18 | GED01-CLIENT | Adaptateur Python invoice2data + profil YAML Fournisseur-EXP-01 candidat | IMPLEMENTED_NOT_TESTED | Interface locale JSON ; extraction OCR non exécutée et non qualifiée |
| 2026-10-18 | Fournisseur-EXP-01-PUBLIC | PNG et PDF expérimentaux visibles dans le dépôt (import manuel) | PUBLISHED_UNQUALIFIED | Présentation issue d'une facture commerciale ; aucune certification d'anonymisation ni de droits |

| 2026-10-18 | HORIZON-FORMAT-001 | Reconnaissance de format par TAG qualifié sur corpus ; architecture conceptuelle déclarée | HORIZON_DECLARED | Voir `documentation/architecture/HORIZON_RECONNAISSANCE_FORMATS.md` ; aucune performance ni implémentation du matcher revendiquée |

| 2026-10-18 | HORIZON-IDENTITY-001 | Identités canoniques, formats, profils et table de correspondance ; échelle ouverte ; 88 821 cité comme exemple arbitraire sans cible ni ordre de grandeur | HORIZON_DECLARED | Voir `documentation/architecture/IDENTITES_CORRESPONDANCES.md` ; aucun volume cible fixé ni inventaire constitué |

## Consolidation du 25 octobre 2026

Les entrées du 18 octobre restent historiques ; elles ne décrivent pas toutes l’état courant. Voir [l’état du projet](ETAT_DU_PROJET.md).

| Date | Référence | Objet | Statut | Preuve / limite |
| --- | --- | --- | --- | --- |
| 2026-10-25 | DEPOT-PUBLIC | Visibilité effective du dépôt | PUBLIC | Métadonnées GitHub vérifiées ; prologue aligné |
| 2026-10-25 | GED01-CONFIDENTIALITE | Validation du spécimen public par le fondateur confirmée | VALIDATED_BY_FOUNDER | Spécimen inchangé ; cette validation ne s’étend pas à d’autres sources |
| 2026-10-25 | GED03-EXECUTION | Phase 1 réalisée et rejeu des neuf courriels synthétiques | TESTED_CANDIDATE | [Résultats](../experiences/administration-droits/GED-03/RESULTS_V0_1.md), sans qualification de production |
| 2026-10-25 | GED04-INSTRUCTION | Instruction terminée et profil candidat produit | CANDIDATE | [Résultat](../experiences/assurances/GED-04/preuves/escalade-consommateur/resultats/ULISDOQ-REQ-GEDREAL-20261024T213000Z-001/result.json), dettes réservées phase 2 |
| 2026-10-25 | GED05-PAYE | Catégorie et grammaire de bulletin de paie français | CANDIDATE_UNQUALIFIED | [Profil canonique](../catalogue/index.json), sources privées exclues |
| 2026-10-25 | DEPOT-RANGEMENT | Chemins francisés et liaisons réparées | TESTED | [22 tests de rangement](preuves/COHERENCE_VERTICALES_2026-10-25.md) |
| 2026-10-25 | BUILDER-CONSOLIDATION | Sélection des matchers intégrée dans Builder 0.1.2 | EVALUATION_CANDIDATE | [Version](../logiciels/profile-builder/RELEASE_0_1_2.md), planification seule |

## Ajouter une entrée

Date, identifiant, objet, statut, lien vers protocole ou preuve vérifiable, auteur/relecteur si publiable, limites et décision explicite. Les informations privées ne figurent jamais dans ce registre.
