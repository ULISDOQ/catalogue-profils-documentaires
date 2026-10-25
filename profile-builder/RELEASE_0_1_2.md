# Profile Builder 0.1.2 — consolidation

Statut : candidat d’évaluation, intégré à la référence courante du dépôt.

Cette version reprend la sélection déterministe des matchers de 0.1.1 : préconditions déclarées, préférence au coût minimal, ambiguïté explicite en cas d’égalité, absence d’exécution des matchers. La politique de sélection reste en version 0.1.1 et GED-core Machine en 0.1.0-candidate.

0.1.2 consolide cette capacité avec les ressources francisées et la distribution courante. Elle ne matérialise pas de profil et ne qualifie aucun profil pour la production.

## Régression GED-03 expliquée

Le plan historique contenait la limite `Synthetic GED-03 corpus only`. Son empreinte canonique est `f33c59d1ad25981ba43e8ec2cce134967c50fc8188b120fe0bbc4681813116d1`.

L’oracle courant contient `Phase-1 synthetic corpus only`. La décision, les capacités et les autres champs sont identiques ; cette différence de texte suffit à modifier l’empreinte en `f0d7ebdde26100b90d4d4680dd1d7f58943d9429a16ea8d0d090dde22d709a68`.

Deux contrôles distincts vérifient désormais le plan courant complet et le rejeu du vecteur historique avec son empreinte d’origine. Aucune preuve figée n’est réécrite et aucune assertion n’est retirée pour masquer l’écart.

## Distribution

Le [manifeste courant](DISTRIBUTION_MANIFEST_0_1_2.json) désigne les fichiers par leurs empreintes Git et le jalon `v0.1.0-alpha.1` du dépôt. La distribution 0.1.1 conserve son manifeste historique et son commit source ; ses empreintes ne désignent pas les fichiers courants après consolidation.

```bash
cd profile-builder
python3 -m ulisdoq_profile_builder info
python3 -m ulisdoq_profile_builder selftest
python3 -m unittest discover -s tests -v
```

Le lanceur `bin/profile-builder` fournit aussi l’entrée locale. Aucun déploiement consommateur n’est inclus dans cette consolidation.
