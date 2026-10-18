# ULISDOQ — Modèle opératoire du projet (POM léger v0.1)

Statut : **candidat de fonctionnement**, indépendant du POM du projet CLAU. Ce document s'inspire de la discipline de traçabilité de CLAU sans transférer ses autorités, secrets ou objets internes.

## Objets et filiation

`besoin → famille documentaire → source autorisée → profil candidat versionné → fixture autorisée → protocole de test → observation → décision de qualification → publication`.

- **Source** : provenance, droits et confidentialité explicités ; les originaux personnels restent hors dépôt.
- **Profil** : identifiant stable, version, famille, critères de reconnaissance, champs, limites.
- **Fixture** : document d'essai dont la publication est autorisée ; lien à un attendu versionné.
- **Exécution** : moteur et version, environnement, date, paramètres, sorties et écarts.
- **Décision** : CANDIDATE, TESTED, QUALIFIED, REJECTED ou WITHDRAWN ; jamais déduite d'une simple création de fichier.

## Horizon architectural déclaré

[HORIZON-FORMAT-001](HORIZON_FORMAT_MATCHER.md) formalise la distinction entre signature observée, TAG de format, profil d'extraction, preuve de qualification et client consommateur. L'architecture vise la récupération de profils par Git/API, la reconnaissance et l'extraction locales, sans ChatGPT en fonctionnement nominal. Ce chantier est un horizon : ses métriques, sa nécessité technique et sa qualification restent à établir.

## Règles de publication

Une copie modifiée d'un document commercial réel n'est pas automatiquement librement redistribuable. La vérification de confidentialité, de droits et des métadonnées précède sa publication. Les éléments non publiables restent dans l'environnement privé autorisé. Aucun fichier public ne doit contenir d'identifiants personnels, de secrets ou de données de santé identifiables.

## Registre

Le registre versionné est `project/LEDGER.md`. Il contient des références publiques et des statuts, pas de données privées. Une nouvelle preuve ou décision ajoute une entrée datée ; on ne réécrit pas l'historique pour embellir les résultats.
