# Profile Builder 0.1.3 — correction du lanceur

Statut : candidat d’évaluation, planification seule.

Le paquet Python était présent, mais `bin/profile-builder` ne le retrouvait pas lors d'un lancement direct. Le lanceur résout désormais sa propre localisation et ajoute la racine du paquet à son chemin d'importation. Aucun changement du planner, des capacités ou des profils.

Depuis un autre répertoire, appeler le chemin absolu du lanceur :

```bash
/chemin/vers/logiciels/profile-builder/bin/profile-builder info
/chemin/vers/logiciels/profile-builder/bin/profile-builder selftest
```

Le même fonctionnement est vérifié sur une distribution reconstruite à partir des seuls fichiers du [manifeste courant](DISTRIBUTION_MANIFEST_ORGANISATION_2.json), archivée puis extraite hors du dépôt. Aucun paquet Python tiers ni installation système n'est nécessaire pour ces commandes. Un interpréteur `python3` doit être disponible pour le lancement direct sous Linux.

Les tests couvrent le script avec Python isolé, le lancement exécutable depuis un répertoire extérieur et le paquet reconstruit : `info`, `selftest`, `plan` avec le registre embarqué par défaut. Le plan GED-03 complet et son empreinte `f0d7ebdde26100b90d4d4680dd1d7f58943d9429a16ea8d0d090dde22d709a68` restent inchangés.

La politique de sélection reste en 0.1.1, GED-core Machine en 0.1.0-candidate. Aucun moteur n'est exécuté par le planner ; aucun profil n'est matérialisé ou qualifié pour la production. Les manifestes historiques 0.1.1 et 0.1.2 conservent leurs octets et leur source exacte. Pour reconstruire 0.1.3, récupérer le commit contenant le manifeste courant et vérifier les empreintes indiquées.

Validation effectuée sous Ubuntu 24.04, Python 3.12.14. Elle ne vaut pas recette sur un autre poste Ubuntu consommateur. Les deux défauts invoice2data relevés séparément restent hors de cette correction.
