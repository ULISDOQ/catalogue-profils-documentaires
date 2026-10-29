# GED-02 — ULISTAG phase 1 : 2044

**Référence : GED02-ULISTAG-PHASE1-001**  
**Statut : CANDIDAT EXPÉRIMENTAL — QUALIFICATION=NONE**

## Intention

Construire un ULISTAG de phase 1 suffisamment stable pour reconnaître plusieurs représentations du même profil documentaire 2044, en réutilisant ULISTAG cœur plutôt qu'en reconstruisant une méthode propre à GED-02.

## Réemploi depuis GED-01

GED-01 a établi l'intérêt de :

- comparer des repères locaux plutôt qu'un score global de page ;
- conserver une cohérence géométrique entre repères ;
- distinguer reconnaissance documentaire, profil et extraction ;
- produire une décision explicable `MATCH_CANDIDATE | UNKNOWN`.

GED-02 conserve ces principes mais rencontre une nouvelle contrainte : la source officielle contient une couche texte exploitable alors que les représentations synthétiques sont image-only.

La brique généralisée choisie est donc un matcher de **points visuels locaux + cohérence géométrique**, capitalisé dans `logiciels/ULISTAG/matchers/visual_keypoints/`.

## Construction initiale

Référence documentaire : PDF officiel `2044_5132.pdf`.

Première représentation d'épreuve : `GED02-S01_2044_2025_SYNTHETIC.pdf`.

Le TAG candidat est construit à partir du rendu du PDF officiel :

```text
4 pages
→ jusqu'à 100 points ORB stables conservés par page
→ coordonnées normalisées
→ descripteurs binaires
→ appariement Hamming
→ homographie RANSAC
```

La représentation S01 est reconnue sur les quatre pages malgré l'ajout de valeurs synthétiques, d'un bandeau de spécimen et une géométrie de rendu différente.

Résultat S01 :

```text
STATUS=MATCH_CANDIDATE
MATCHING_PAGES=4/4
QUALIFICATION=NONE
```

## Épreuves successives

Conformément au protocole de phase 1, les variantes sont ensuite éprouvées séparément avec la même référence et le même matcher :

| Spécimen | Résultat | Pages reconnues |
|---|---|---:|
| S01 | MATCH_CANDIDATE | 4/4 |
| S02 | MATCH_CANDIDATE | 4/4 |
| S03 | MATCH_CANDIDATE | 4/4 |
| S04 | MATCH_CANDIDATE | 4/4 |
| S05 | MATCH_CANDIDATE | 4/4 |
| S06 | MATCH_CANDIDATE | 4/4 |
| S07 | MATCH_CANDIDATE | 4/4 |
| S08 | MATCH_CANDIDATE | 4/4 |

Le témoin négatif fiscal ressemblant est testé ensuite :

```text
GED02-N01_FISCAL_LOOKALIKE_NEGATIVE_SYNTHETIC
STATUS=UNKNOWN
MATCHING_PAGES=0/4
```

## Politique candidate

```text
ratio_test=0.72
ransac_reproj_px=5.0
min_good_matches=35
min_inliers=25
min_inlier_ratio=0.55
min_matching_pages_ratio=0.75
```

Ces seuils sont des paramètres expérimentaux de phase 1. Ils ne constituent ni une probabilité ni une qualification.

## Interprétation

Cette expérience montre qu'une même brique ULISTAG cœur peut reconnaître :

- le rendu du formulaire officiel ;
- plusieurs représentations synthétiques modifiées du même modèle ;
- y compris lorsque la couche texte n'est pas disponible ;

tout en rejetant le témoin négatif fourni.

Elle ne démontre pas la robustesse générale sur d'autres millésimes, scans réels, déformations fortes ou formulaires fiscaux voisins non inclus dans cette expérience.

## Dette pour phase 2

Ne pas perfectionner ce TAG maintenant. Capitaliser les observations de phase 1 puis réexaminer, après accumulation des cas GED-N :

- taille optimale du TAG ;
- indexation rapide dans un catalogue volumineux ;
- choix et fusion des primitives ;
- calibrage des seuils ;
- faux positifs et faux négatifs sur corpus indépendant ;
- robustesse aux millésimes et transformations réelles.


## Référence canonique immuable

Le descripteur utilisé pour Gate A est désormais matérialisé comme artefact versionné.

```text
REFERENCE_VERSION=0.1
RESTORED_FILE=reference_visual_v0_1.json
SHA256=8950bbaf084e02ceab841835e72287a369cc77e999332af55c1c893dd7704e24
SIZE=70043
```

Le dépôt conserve cet artefact sous forme compressée découpée en quatre parties texte. `restore_reference_visual_v0_1.py` ne calcule aucun point ORB : il décode uniquement l'artefact canonique et refuse toute dérive de hash.

Pour S11 : **aucune reconstruction, recalibration ou modification de seuil n'est autorisée**.
