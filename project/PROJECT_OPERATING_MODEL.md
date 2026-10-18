# ULISDOQ — Modèle opératoire du projet (POM léger v0.1)

Statut : **candidat de fonctionnement propre à ULISDOQ**. Ce modèle est autonome et n'importe aucune autorité, donnée privée ou dépendance d'un projet extérieur.

## Fonction d'unification

ULISDOQ référence et qualifie des **briques techniques parmi N** (lecture, OCR, reconnaissance, extraction, validation, indexation), avec capacités, versions, interfaces, droits et preuves. Le choix du moteur appartient au contrat de compatibilité du profil, pas à l'identité d'ULISDOQ. Voir [UNIFICATION_TECHNICAL_COMPONENTS.md](UNIFICATION_TECHNICAL_COMPONENTS.md).

## Objets et filiation

`besoin → famille documentaire → source autorisée → profil candidat versionné → fixture autorisée → protocole de test → observation → décision de qualification → publication`.

- **Source** : provenance, droits et confidentialité explicités ; les originaux personnels restent hors dépôt.
- **Profil** : identifiant stable, version, famille, critères de reconnaissance, champs, limites.
- **Fixture** : document d'essai dont la publication est autorisée ; lien à un attendu versionné.
- **Exécution** : moteur et version, environnement, date, paramètres, sorties et écarts.
- **Décision** : CANDIDATE, TESTED, QUALIFIED, REJECTED ou WITHDRAWN ; jamais déduite d'une simple création de fichier.

## Identité canonique et horizontalité

[HORIZON-IDENTITY-001](HORIZON_IDENTITY_MAPPING.md) définit les objets distincts entité, alias, format, profil et correspondance. Aucun nom commercial ne doit être nécessaire dans les identifiants canoniques des profils. L'échelle du référentiel reste ouverte ; aucun nombre cible d'entités n'est fixé.

## Horizon architectural déclaré

[HORIZON-FORMAT-001](HORIZON_FORMAT_MATCHER.md) formalise la distinction entre signature observée, TAG de format, profil d'extraction, preuve de qualification et client consommateur. L'architecture vise la récupération de profils par Git/API, la reconnaissance et l'extraction locales, sans ChatGPT en fonctionnement nominal. Ce chantier est un horizon : ses métriques, sa nécessité technique et sa qualification restent à établir.

## Règles de publication

Une copie modifiée d'un document commercial réel n'est pas automatiquement librement redistribuable. La vérification de confidentialité, de droits et des métadonnées précède sa publication. Les éléments non publiables restent dans l'environnement privé autorisé. Aucun fichier public ne doit contenir d'identifiants personnels, de secrets ou de données de santé identifiables.

## Registre

Le registre versionné est `project/LEDGER.md`. Il contient des références publiques et des statuts, pas de données privées. Une nouvelle preuve ou décision ajoute une entrée datée ; on ne réécrit pas l'historique pour embellir les résultats.
