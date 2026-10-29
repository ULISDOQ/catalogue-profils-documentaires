# État courant d’ULISDOQ

Jalon : **0.1.0-alpha.1 — consolidation du 25 octobre 2026**.

`main` est la référence courante et la branche de travail du projet, y compris pour les travaux en évaluation. Toute nouvelle branche exige une décision ou une confirmation explicite de Jean avant sa création. Le dépôt est public. Ce jalon décrit un état d’évaluation reconstructible ; aucun profil n’est déclaré qualifié pour la production.

| Surface | État courant | Référence |
| --- | --- | --- |
| Catalogue | Profil canonique candidat de bulletin de paie français, non sélectionnable automatiquement | [Index](../catalogue/index.json) |
| Client | Capacité générique séparée des expériences ; TAG, résolution, extraction locale | [Client](../logiciels/client/README.md) |
| ULISTAG | Matchers candidats et référence visuelle GED-02 conservée avec empreintes | [ULISTAG](../logiciels/ULISTAG/README.md) |
| Profile Builder | 0.1.3, lanceur autonome corrigé ; sélection des matchers intégrée, planification seule | [Version courante](../logiciels/profile-builder/RELEASE_0_1_3.md) |
| GED-01 | Spécimens publics validés par le fondateur ; candidat, stabilité intra-modèle à approfondir | [Expérience](../experiences/factures/GED-01/README.md) |
| GED-02 | Reconnaissance/extraction expérimentales ; robustesse sémantique partielle, dont ligne 420 | [Dette](../experiences/impots-finances/GED-02/profils/DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001.md) |
| GED-03 | Six positifs et trois négatifs/limites synthétiques ; parseur et validation éprouvés | [Résultats](../experiences/administration-droits/GED-03/RESULTS_V0_1.md) |
| GED-04 | Instruction terminée, profil candidat construit, réemploi indépendant non qualifié | [Dette phase 2](../experiences/assurances/GED-04/DETTE_PHASE_2.md) |
| GED-05 | En pause à la décision de Jean ; catégorie et grammaire candidates, chaîne terrain non validée, sources privées exclues du dépôt | [Expérience](../experiences/paye/GED-05/README.md) |

Les candidats conservés dans les expériences restent distincts du catalogue canonique. Leur présence ne vaut ni promotion dans le catalogue ni qualification.

## Reprendre ou reconstruire

1. Lire cette page, puis [l’organisation du dépôt](architecture/ORGANISATION_DU_DEPOT.md).
2. Récupérer `main` et noter son commit exact pour reproduire cet état. Le tag `v0.1.0-alpha.1` est prévu mais sa création reste en attente.
3. Suivre [la vérification du dépôt](../logiciels/verification/VERIFIER_LE_DEPOT.md).
4. Consulter les expériences et preuves uniquement lorsque le travail l’exige.

Les versions ont des périmètres distincts : jalon du dépôt `0.1.0-alpha.1`, logiciel Builder `0.1.3`, versions propres à chaque profil. Une version de dépôt ne qualifie pas automatiquement ces objets.

L'audit de stabilité du 29 octobre a révélé trois défauts antérieurs au rangement. Le lanceur du Builder est corrigé en 0.1.3. L'installation neuve d'invoice2data est corrigée par la dépendance de compatibilité `setuptools==80.9.0`, qui fournit `pkg_resources` ; déclarations et contrôle de déploiement sont alignés. L'adaptateur facture transmet encore un nom de lecteur à une API qui attend un module. La stabilité globale du profil de déploiement complet reste donc non acquise.

## Suite

Poursuivre l’exploration documentaire de phase 1. Les dettes de robustesse, performance et qualification approfondie GED-02/GED-04 restent réservées à la phase 2 ; la consolidation du logiciel existant ne les relance pas.

Le [registre](JOURNAL_DECISIONS.md) conserve les décisions datées ; cette page présente leur état courant. Les contrôles de confidentialité précèdent toute publication de nouveau spécimen. La validation déjà donnée pour GED-01 reste acquise.

## Branches secondaires supprimées

Suppression effectuée par Jean et vérifiée le 25 octobre 2026 : seule `main` reste présente. Son commit était inchangé à `acab1b593a6887b8d791af71440a138ea03edecb` après suppression. Les trois anciens sommets restent ancêtres de main : aucun travail ni historique utile n’a été perdu.

Toute nouvelle branche exige toujours une décision ou confirmation explicite de Jean. Le tag `v0.1.0-alpha.1` reste non créé ; la reconstruction fonctionne par commit exact et le manifeste du Builder ne dépend pas de ce tag.
