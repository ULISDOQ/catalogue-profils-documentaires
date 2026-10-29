# Correction du rangement et cohérence des verticales

Date : 25 octobre 2026. Base : `17d3a2906e6564c14c1f09ca0e9e95e23b6b5fce`.

## Résultat

**PASS pour la cohérence du rangement : 22 tests réussis.**

| Suite | Tests | Résultat |
| --- | ---: | --- |
| Cohérence des ressources et verticales | 11 | PASS |
| Client TAG | 3 | PASS |
| Profile Builder | 3 | PASS |
| Escalade consommateur | 5 | PASS |

Les références actives utilisent `experiences/` et les sous-dossiers réels : `profils/`, `specimens/`, `modeles/`, `contrats/`, `phase2-reentree/`, `preuves/`, `documentation/`. Les options d'API telles que `--templates` et les identifiants de schéma restent inchangés.

## Ce qui a été vérifié

- Absence d'ancienne racine dans les références actives ; existence des ressources visées et des liens Markdown relatifs.
- Registre des profils : résolution des profils, adaptateurs, schémas et références ULISTAG ; correspondance des empreintes Git des profils avec leurs octets actuels.
- Registre des capacités : existence des adaptateurs et des preuves déclarées.
- GED-01 : ressources relatives du profil, du graphe et du cas de test ; spécimens PDF/PNG inchangés.
- GED-02 : décodage des quatre parties de la référence visuelle et vérification des empreintes comprimée/décomprimée et de la taille ; validation du schéma de l'extraction figée ; rapprochement avec l'oracle synthétique en conservant l'écart connu de ligne 420.
- GED-03 : résolution native du profil, rejeu des neuf courriels synthétiques, validation JSON Schema et comparaison aux statuts/champs/attachements de l'oracle indépendant.
- GED-04 : cohérence demande → accusé → résultat → profil candidat, corrélation, rejet d'une déclaration de source privée, absence de double acceptation productive.
- GED-05 : index → profil → grammaire/preuves/qualification ; maintien du statut candidat non qualifié et non sélectionnable automatiquement.
- Déploiement : destination du schéma chargé par le vérificateur complet et ressources de l'inventaire de capacités. Aucun déploiement PCIA n'a été effectué.

## Écarts préexistants clarifiés

Les tests d'escalade chargeaient d'anciens répertoires et attendaient l'ancien résultat GED-04. Le résultat courant est `COMPLETED` / `NEW_PROFILE_CANDIDATE_REQUIRED`, avec profil candidat et demande de preuve indépendante pour la suite. Les tests contrôlent cet état sans prétendre qualifier le profil.

Le rejeu du Builder échouait aussi sur une reformulation de limite de corpus. Le registre reprend la formulation de l'oracle historique, de sens équivalent ; le plan attendu et les assertions ne sont pas affaiblis.

GED-02 : le test retrouve explicitement l'écart historique de ligne 420 (`591` extrait, `5910` attendu). Cette dette reste ouverte en phase 2. PASS désigne ici la cohérence de la référence, des ressources et des limites déclarées, pas une extraction intégralement exacte.

## Preuves historiques

Le bundle figé GED-03 conserve exactement ses octets et ses localisateurs d'époque. La [correspondance historique](../../experiences/administration-droits/GED-03/preuves/CORRESPONDANCE_CHEMINS_HISTORIQUES.json) donne les chemins actuels et l'empreinte du bundle conservé. Les deux localisateurs anciens qui subsistent ne sont pas des chemins actifs à utiliser.

## Visibilité et sources privées

Visibilité GitHub vérifiée : **public**. Le prologue décrit désormais cette situation effective.

Contrôle de l'état initial : 191 fichiers sur main, branches distantes accessibles et historique Git récupéré (2 269 objets). Recherche ciblée des identifiants personnels connus : aucune occurrence détectée dans les noms/contenus des blobs examinés. Il ne s'agit pas d'une preuve universelle d'absence de toute donnée personnelle ni d'un audit des issues, actions, forks ou copies externes.

Les seuls fichiers PDF/PNG trouvés dans les objets accessibles correspondent au spécimen GED-01 déjà validé par le fondateur comme ne révélant rien de privé. Les deux pages PNG ont été examinées ; les images incorporées au PDF leur sont identiques, sans texte caché, annotation ou métadonnée personnelle observée. Les valeurs du spécimen sont conservées conformément à cette validation.

Les courriels GED-03 utilisent des adresses synthétiques ; les résultats fiscaux S11 sont synthétiques. Les originaux privés GED-04/GED-05 ne figurent pas dans l'arbre examiné. Les règles de contribution précisent le contrôle préalable à toute publication de nouveau spécimen ; les exclusions Git de dossiers privés constituent une précaution, pas une garantie automatique d'anonymisation.

## Reproduire

Dans un environnement disposant de `jsonschema` (version exécutée : 4.25.1) :

```bash
python3 -m unittest discover -s logiciels/verification/tests -v
(cd logiciels/client && python3 test_tag_candidate.py)
(cd logiciels/profile-builder && python3 -m unittest discover -s tests -v)
python3 -m unittest discover -s logiciels/escalade-consommateur/tests -v
git diff --check
```

Le test de cohérence se trouve dans [test de cohérence](../../logiciels/verification/tests/test_coherence_verticales.py). Les moteurs OCR, invoice2data et OpenCV n'ont pas été réinstallés ni qualifiés par ce contrôle de rangement. Aucun document personnel source n'a été ajouté.
