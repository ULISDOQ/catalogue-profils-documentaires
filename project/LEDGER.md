# ULISDOQ — Ledger versionné

Version de structure : **0.1**. Les commits Git constituent l'historique technique ; ce registre porte les décisions et les limites de qualification.

| Date | Référence | Objet | Statut | Preuve / limite |
|---|---|---|---|---|
| 2026-10-18 | IDENTITY-001 | ULISDOQ et lignage ULIS/DOCQ/DOCK | DOCUMENTED | Voir `PROLOGUE_FONDATEUR.md` |
| 2026-10-18 | GED-01 | Première expérience de facture fictive | CANDIDATE | Fixtures et tests définis ; aucune extraction exécutée |
| 2026-10-18 | Fournisseur-EXP-01 | Dérivé expérimental d'une facture Fournisseur-EXP-01 réelle | PRIVATE_REVIEW_REQUIRED | Deux images et PDF image-only préparés hors dépôt ; contrôle confidentialité et droits de publication non achevé |
| 2026-10-18 | GED-01-EXEC | Évaluation du moteur de reconnaissance/extraction | NOT_RUN | Aucune mesure de performance ni qualification revendiquée |


| 2026-10-18 | Fournisseur-EXP-01-SVG | Deux reconstitutions visuelles publiques de la facture Fournisseur-EXP-01 transformée | PUBLISHED_RECONSTRUCTION | SVG lisibles, non équivalents aux PNG/PDF image-only ; aucune preuve OCR | 

| 2026-10-18 | GED01-SIMPLIFY | Suppression des deux SVG redondants et parcours de lecture unique | DONE | Voir `experiments/GED-01/README.md` |
| 2026-10-18 | GED01-CLIENT | Adaptateur Python invoice2data + profil YAML Fournisseur-EXP-01 candidat | IMPLEMENTED_NOT_TESTED | Interface locale JSON ; extraction OCR non exécutée et non qualifiée |
| 2026-10-18 | Fournisseur-EXP-01-PUBLIC | PNG et PDF expérimentaux visibles dans le dépôt (import manuel) | PUBLISHED_UNQUALIFIED | Présentation issue d'une facture commerciale ; aucune certification d'anonymisation ni de droits |

| 2026-10-18 | HORIZON-FORMAT-001 | Reconnaissance de format par TAG qualifié sur corpus ; architecture conceptuelle déclarée | HORIZON_DECLARED | Voir `project/HORIZON_FORMAT_MATCHER.md` ; aucune performance ni implémentation du matcher revendiquée |

| 2026-10-18 | HORIZON-IDENTITY-001 | Identités canoniques, formats, profils et table de correspondance ; cible de dimensionnement 88 821 entités | HORIZON_DECLARED | Voir `project/HORIZON_IDENTITY_MAPPING.md` ; aucun registre de 88 821 entités constitué |

## Ajouter une entrée

Date, identifiant, objet, statut, lien vers protocole ou preuve vérifiable, auteur/relecteur si publiable, limites et décision explicite. Les informations privées ne figurent jamais dans ce registre.
