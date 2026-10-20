# ULISTAG GED-01 — Graphe d'ancres structurelles v0.1

**Référence : ULISTAG-GED01-ANCHOR-GRAPH-001**  
**Statut : CANDIDAT EXPÉRIMENTAL NON QUALIFIÉ**  
**Origine : proposition de Jean, instruite dans ULISDOQ**  
**Cas d'épreuve : GED-01 / facture mobile SFR**

## 1 — Sources effectivement examinées

La conception v0.1 a été établie à partir de deux représentations du même modèle documentaire :

- la facture source privée, déposée par Jean dans la Bibliothèque ChatGPT et consultée uniquement pour l'étude ; elle n'est ni copiée ni publiée dans le dépôt ;
- les deux pages publiques transformées de GED-01 :
  - `experiments/factures/GED-01/fixtures/Fournisseur-EXP-01_page_1.png`
  - `experiments/factures/GED-01/fixtures/Fournisseur-EXP-01_page_2.png`

Les deux représentations conservent la même organisation générale : deux pages, zones de titre, ligne d'identification de facture, bloc de synthèse, sections de détail et repères de pagination. Les valeurs privées ou variables ne sont pas retenues dans l'empreinte.

## 2 — Constat déterminant du RETEX

L'aplatissement d'un PDF en simple texte peut perdre la relation spatiale entre un libellé et sa valeur. Dans le cas étudié, une expression régulière appliquée au texte aplati peut associer au libellé du montant une valeur voisine qui n'est pas le montant total attendu.

Ce constat justifie de conserver la géométrie dans le chemin nominal :

```text
texte + coordonnées
→ ancres stables
→ relations géométriques
→ candidat de modèle
→ profil structurel
→ extraction relative aux ancres
```

La reconnaissance et l'extraction restent deux décisions distinctes.

## 3 — Méthodes envisagées

### A — Comparaison de pixels / grille globale

Simple et rapide mais trop sensible aux valeurs variables, aux zones modifiées et aux décalages. Le RETEX GED-01 a déjà montré qu'un score global ne suffit pas pour décider du modèle.

**Décision : non retenu comme mécanisme principal.**

### B — Encodage global du layout

Les travaux de Hu, Kashi et Wilfong montrent qu'une représentation compacte de la disposition peut être efficace pour comparer des pages sans OCR.

**Intérêt :** rapide et utile comme préfiltre.  
**Limite pour ULISDOQ :** moins explicable lorsqu'il faut dire quels éléments du modèle correspondent et pourquoi.

**Décision : piste secondaire / préfiltre possible.**

### C — Graphe général + graph edit distance

Les blocs deviennent des nœuds et les relations spatiales des arêtes. Un algorithme général de distance d'édition de graphes pourrait ensuite chercher la meilleure correspondance.

**Intérêt :** expressif.  
**Limites :** complexité inutile pour un premier catalogue lorsque les nœuds peuvent déjà être nommés par des ancres stables ; coût et réglage plus difficiles à expliquer.

**Décision : non retenu en v0.1.**

### D — Graph matching appris

LayoutGMN illustre la puissance des réseaux de graph matching pour apprendre une similarité structurelle entre layouts.

**Intérêt :** pertinent pour des corpus larges et des variations complexes.  
**Limites :** nécessite un corpus d'apprentissage, une métrique apprise et davantage de calcul ; trop lourd avant d'avoir démontré l'insuffisance d'une méthode déterministe.

**Décision : réservé à une éventuelle étape ultérieure.**

### E — Graphe d'ancres nommées + cohérence géométrique

Méthode retenue en v0.1.

Les nœuds sont des **ancres textuelles stables** ne contenant pas de donnée personnelle. Chaque nœud porte :

- page ;
- libellé normalisé ;
- centre géométrique normalisé ;
- tolérance de position.

Les arêtes relient quelques ancres structurantes et portent la relation géométrique attendue. La comparaison vérifie séparément :

1. la présence des ancres ;
2. leur position relative ;
3. la cohérence des relations du graphe ;
4. le nombre de pages.

Cette méthode reprend l'idée de **repères locaux reliés entre eux** présente dans les systèmes d'empreinte comme celui décrit par Avery Wang, mais sans reproduire un mécanisme audio et sans transformer les relations en simple hash opaque.

## 4 — Pourquoi cette méthode est élue

Pour GED-01, les correspondances sont déjà fortement contraintes par des ancres lisibles et stables. Il n'est donc pas nécessaire de résoudre un problème général d'isomorphisme de graphes.

Le graphe d'ancres nommées est retenu parce qu'il est :

- **simple** : quelques nœuds et relations ;
- **déterministe** : aucune phase d'apprentissage ;
- **explicable** : un écart peut être rattaché à une ancre ou une relation précise ;
- **robuste au contenu variable** : numéros, dates, montants et identité client ne participent pas à l'identité du modèle ;
- **compatible avec plusieurs lecteurs** : couche texte PDF aujourd'hui, OCR demain ;
- **indexable** : les ancres communes peuvent générer rapidement des candidats avant vérification géométrique.

## 5 — ULISTAG candidat GED-01

Référence :

`experiments/factures/GED-01/ulistag/reference_v0_1.json`

Le candidat comporte dix ancres non privées :

Page 1 :
- `VOTRE FACTURE MOBILE`
- `FACTURE N°`
- `Montant net à prélever`
- `Montant facturé`
- `Dont TVA`

Page 2 :
- `Votre facture en détail`
- `VOS ABONNEMENTS, FORFAITS ET OPTIONS`
- `VOS CONSOMMATIONS TÉLÉPHONIQUES`
- `Compris dans vos forfaits`
- `Compris dans votre forfait précédent`

Les coordonnées de référence ont été initialisées à partir de la source privée pour obtenir une mesure précise, puis la présence et la disposition de ces mêmes ancres ont été contrôlées sur les fixtures publiques. C'est un **amorçage de conception**, pas une validation indépendante.

## 6 — Comparateur v0.1

Implémentation :

`client/ulistag_v0.py match`

Le résultat est :

- `MATCH_CANDIDATE` si le nombre de pages, la proportion d'ancres et la cohérence des arêtes satisfont la politique candidate ;
- `UNKNOWN` sinon.

Dans un catalogue multi-références, `AMBIGUOUS` sera ajouté lorsque plusieurs candidats restent compatibles.

Les ratios produits signifient uniquement **compatibilité structurelle selon ce règlement**. Ils ne sont pas des probabilités.

## 7 — Profil d'extraction structurel associé

Référence :

`experiments/factures/GED-01/profiles/sfr_structural_v0_1.json`

Le profil extrait les champs en utilisant les ancres et la géométrie, au lieu de supposer que l'ordre du texte aplati préserve la proximité visuelle.

Le candidat actuel définit trois stratégies minimales :

- valeur comprise entre une ancre et un token de fin sur la même ligne ;
- valeur située après un token sur la même ligne ;
- valeur située dans une bande à droite de l'ancre sur la même ligne.

Une implémentation candidate avec `pdfplumber` est fournie, mais **pdfplumber n'est pas une obligation du contrat ULISTAG**.

## 8 — Essai dans l'environnement ChatGPT

La facture source privée a été rendue et inspectée localement. Le candidat v0.1 a ensuite été exécuté sans publier les valeurs extraites.

Résultat de reconnaissance :

```text
STATUS=MATCH_CANDIDATE
PAGE_COUNT=2
NODE_RATIO=1.0
EDGE_RATIO=1.0
QUALIFICATION=NONE
```

Résultat d'extraction minimisé :

```text
invoice_number=EXTRACTED
date=EXTRACTED
amount=EXTRACTED
STATUS=EXTRACTED_UNVERIFIED
```

Ce résultat démontre uniquement que le mécanisme candidat fonctionne sur **ce document utilisé pendant la conception**. Il ne constitue ni un test indépendant ni une qualification.

## 9 — Protocole suivant

1. exécuter le même client sur la source réelle depuis PCIA ;
2. retourner uniquement les statuts et écarts minimisés ;
3. exécuter le règlement sur A/B synthétiques de même structure ;
4. ajouter au moins un négatif de structure différente ;
5. vérifier qu'une variation des valeurs ne modifie pas l'identité structurelle ;
6. vérifier qu'une variation structurelle significative provoque `UNKNOWN` ;
7. seulement ensuite, constituer un corpus indépendant pour estimer faux rapprochements et faux rejets.

## 10 — Bibliographie utilisée

- Avery Li-Chun Wang, **An Industrial-Strength Audio Search Algorithm**, ISMIR 2003. DOI/archivage : https://doi.org/10.5281/zenodo.1416340
- Jianying Hu, Ramanujan S. Kashi, Gordon T. Wilfong, **Comparison and Classification of Documents Based on Layout Similarity**, *Information Retrieval* 2, 227-243, 2000. DOI : https://doi.org/10.1023/A:1009910911387
- Reza Azmi et al., **LGL-DIR: Layout graph for layout based document image retrieval**, ICETC 2010. DOI : https://doi.org/10.1109/ICETC.2010.5529685
- Akshay Gadi Patil et al., **LayoutGMN: Neural Graph Matching for Structural Layout Similarity**, CVPR 2021. DOI : https://doi.org/10.1109/CVPR46437.2021.01090
- Yiheng Xu et al., **LayoutLM: Pre-training of Text and Layout for Document Image Understanding**, KDD 2020. Référence : https://kdd.org/kdd2020/accepted-papers/view/layoutlm-pre-training-of-text-and-layout-for-document-image-understanding.html

## 11 — Limites explicites

- une seule source réelle a participé à la conception ;
- les coordonnées ont donc besoin d'une validation indépendante ;
- les tolérances sont expérimentales ;
- le lecteur v0.1 suppose un PDF à couche texte exploitable ;
- les scans nécessiteront un adaptateur OCR fournissant les mêmes ancres et coordonnées ;
- le graphe v0.1 est volontairement petit et ne cherche pas à représenter toute la page ;
- aucun taux de reconnaissance généralisable n'est revendiqué.
