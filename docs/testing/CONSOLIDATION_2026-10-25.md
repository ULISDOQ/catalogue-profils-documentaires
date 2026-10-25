# Consolidation du dépôt — 25 octobre 2026

Base : `4734d0e9aa5748f64813d71abc0cb3445524d8dc`. Jalon visé : `v0.1.0-alpha.1`.

## Intégration

La sélection des matchers issue de la branche Builder 0.1.1 rejoint la référence courante en version 0.1.2. Le registre francisé de main est conservé. Les plans courant et historique GED-03 sont vérifiés séparément : la reformulation d’une limite explique exactement leur différence d’empreinte, sans changement de décision ni de capacités choisies.

La documentation distingue maintenant l’état courant des préparations historiques. Le README renvoie vers l’état du projet et une procédure unique de vérification.

## Conservation des branches

| Ancienne branche | Dernier commit avant consolidation | Traitement |
| --- | --- | --- |
| `feat/consumer-escalation-v1-ged04-proof` | `cf5ea5beb6f2853d2c05b425a4ffef273145ca2a` | Déjà ancêtre de main ; fermeture après intégration finale |
| `feat/ged05-payslip-catalogue-first-v0.1` | `79ca9fc9b55d675493b2c332faa33a3858669601` | Changements déjà présents ; historique ajouté comme parent de la consolidation |
| `feat/profile-builder-matcher-selection-0.1.1` | `57371110aff4dce8765498c1d6a9f0bca29c15c6` | Évolution reprise et historique ajouté comme parent de la consolidation |

Le commit de consolidation conserve les historiques, tout en choisissant explicitement l’arbre corrigé et testé. Les branches fermées restent recréables à partir de ces commits ; aucun historique n’est réécrit et aucun force-push n’est nécessaire. Les anciennes URL de branche peuvent cesser de fonctionner ; les références par commit restent valables.

## Validation

Résultat sur l’arbre consolidé : **31 tests PASS** (cohérence 12, client 3, Builder 11, escalade 5), plus autocontrôle du Builder PASS. La reconstruction est vérifiée depuis un nouveau clone, avec son propre environnement virtuel et les seules dépendances de test déclarées. Le premier contrôle a révélé que le scanner parcourait aussi les bibliothèques de cet environnement ; les répertoires de dépendances sont désormais exclus du contrôle des ressources du projet.

La procédure [VERIFIER_LE_DEPOT.md](VERIFIER_LE_DEPOT.md) exécute les contrôles de cohérence, le client, le Builder, son autocontrôle et le contrat d’escalade. Le manifeste courant du Builder est vérifié par les empreintes de ses fichiers. Les preuves figées et les spécimens PDF/PNG GED-01 sont conservés.

Les dettes GED-02/GED-04 restent ouvertes ; ce jalon ne qualifie ni tous les profils, ni les moteurs OCR/OpenCV/invoice2data, ni un déploiement consommateur.

## Situation de clôture

La consolidation a rejoint main au commit `bc23537e934140288ea66e3e34f73c431e8159d5`, qui conserve les deux historiques divergents comme parents supplémentaires. La correction de reconstruction propre a suivi au commit `1d0f8b17ece6c1c77a8380182e6064b0fb3015bc`. Les trois anciens sommets de branche sont désormais ancêtres de main.

La suppression des trois noms de branches et la création du tag ne sont pas réalisées : la connexion sécurisée du navigateur a été refusée par le contrôle automatique avant saisie d’identifiants. Aucun contournement ni changement de permissions n’a été tenté. Les commandes de reconstruction utilisent main et son commit exact ; le manifeste du Builder conserve ses empreintes et un commit source explicite.
