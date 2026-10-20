# ULISTAG — Empreinte structurelle documentaire comparable

**Référence : ULISTAG-RESEARCH-001**  
**Statut : proposition de recherche rattachée à HORIZON-FORMAT-001**  
**Origine de la proposition : Jean**  
**Gouvernance du chantier : ULISDOQ autonome ; CLAU/GED-RÉEL intervient comme consommateur-testeur**  
**Date d'instruction : 2026-10-18**

## 1 — Positionnement

ULISTAG est le **nom candidat de l'empreinte structurelle documentaire comparable** envisagée dans le cadre de HORIZON-FORMAT-001.

ULISTAG n'est :

- ni un identifiant opaque ;
- ni un hash cryptographique classique ;
- ni un profil d'extraction ;
- ni une qualification automatique du document ;
- ni un nouveau projet architectural indépendant.

L'objectif est de représenter des caractéristiques relativement invariantes d'un **modèle documentaire** afin de rapprocher des documents structurellement similaires malgré les variations de contenu, de dates, de montants, de numéros, d'altérations locales et de représentation PDF.

## 2 — Repère pédagogique : comparaison avec Shazam

La référence à Shazam est conservée ici comme **repère pédagogique et source bibliographique de recherche**, et non comme identité d'ULISDOQ, dépendance technique ou déclaration d'une reproduction de ses mécanismes.

L'algorithme décrit par Avery Wang pour Shazam repose sur une réduction du signal audio en **points caractéristiques robustes**, organisés en carte de constellation. Des points ancres sont appariés à des points d'une zone cible ; chaque paire produit une empreinte combinant deux fréquences et leur différence temporelle. La recherche ne se contente pas de compter des collisions de hashes : elle vérifie aussi la **cohérence des décalages temporels** entre les correspondances.

Les idées transposables sont donc moins « faire un hash » que :

1. sélectionner des caractéristiques locales robustes ;
2. construire des relations entre caractéristiques ;
3. produire des tokens comparables suffisamment discriminants ;
4. indexer ces tokens ;
5. agréger les correspondances ;
6. vérifier leur cohérence géométrique globale ;
7. calibrer la décision en fonction des faux positifs acceptables.

### Transposition candidate

| Shazam | ULISTAG |
|---|---|
| Signal audio | Structure documentaire |
| Pic temps-fréquence | Repère structurel documentaire |
| Carte de constellation | Constellation de repères documentaires |
| Relation temporelle | Relation spatiale / topologique |
| Paire ancre-cible | Relation entre deux repères |
| Hash combinatoire | Token structurel comparable |
| Cohérence des offsets | Cohérence des transformations spatiales |
| Track candidate | Modèle documentaire candidat |

### Limite fondamentale de l'analogie

Shazam cherche essentiellement à reconnaître **le même enregistrement** malgré le bruit, la compression ou les perturbations.

ULISTAG vise à reconnaître **le même modèle documentaire** alors que de larges portions du contenu sont légitimement différentes.

La variable à neutraliser n'est donc pas seulement du bruit : elle fait partie de la production normale du document. Un ULISTAG robuste doit distinguer explicitement :

- structure stable ;
- contenu variable ;
- éléments de version ;
- variations admissibles ;
- ruptures de modèle.

## 3 — État de l'art pertinent

### 3.1 Similarité de layout documentaire

Des travaux antérieurs comparent et classent déjà des documents au niveau de leur **layout spatial**, parfois sans OCR. Des méthodes classiques encodent la disposition de régions dans des vecteurs structuraux ; d'autres utilisent des descripteurs locaux robustes répartis dans des partitions hiérarchiques.

Cet acquis confirme qu'une comparaison structurelle documentaire ne doit pas être réduite à un simple taux global de pixels.

### 3.2 Graphes de layout et relations spatiales

Des travaux de document image retrieval représentent les blocs documentaires comme des **graphes de layout** puis comparent leurs chemins ou leurs relations.

Des travaux plus récents, comme LayoutGMN, montrent qu'un graphe explicite des éléments de layout et de leurs relations peut mieux représenter la similarité structurelle que des métriques pixel-à-pixel. Le champ moderne de document structure analysis va également vers des graphes décrivant relations spatiales, ordre de lecture et hiérarchie.

Cet axe est directement compatible avec l'intuition ULISTAG :

`repères → relations → constellation / graphe → comparaison structurée`.

### 3.3 Représentations texte + layout + image

LayoutLM et ses successeurs démontrent l'intérêt de combiner contenu textuel, coordonnées de layout et information visuelle pour comprendre des documents riches.

Pour ULISTAG, cela constitue une preuve que **texte et géométrie peuvent être complémentaires**, mais pas une obligation d'utiliser un modèle appris. La stratégie ULISDOQ reste : réemployer le mécanisme le plus simple satisfaisant les critères.

### 3.4 Perceptual hashing

Le perceptual hashing cherche des représentations similaires pour des images visuellement identiques ou proches. Il est utile pour détection de doublons et near-duplicates, mais il peut être trop sensible au contenu variable d'un document, ou au contraire trop peu explicable pour distinguer structure et données.

Il peut donc servir de **feature auxiliaire**, mais n'est pas assimilé à ULISTAG.

## 4 — Définition candidate d'un ULISTAG

Un ULISTAG candidat est une **empreinte structurée, versionnée et comparable** composée de primitives et de relations.

### 4.1 Primitives structurelles candidates

- géométrie de page normalisée ;
- nombre de pages ou classes de pagination ;
- blocs de texte stables ;
- lignes et séparateurs ;
- zones fonctionnelles ;
- tableaux ;
- images / logos sous forme de caractéristiques non sensibles ;
- densité et distribution de texte ;
- alignements ;
- ancres textuelles stables ;
- régions vides significatives ;
- répétitions inter-pages.

Chaque primitive porte au minimum :

- type ;
- page ;
- géométrie normalisée ;
- niveau de confiance ;
- statut `STABLE_CANDIDATE | VARIABLE | VERSION_FEATURE | UNKNOWN`.

### 4.2 Relations candidates

Relations spatiales normalisées, par exemple :

- gauche / droite ;
- au-dessus / au-dessous ;
- alignement horizontal / vertical ;
- proximité ;
- inclusion ;
- chevauchement ;
- distance relative ;
- ratio de dimensions ;
- appartenance à une même zone ;
- répétition sur plusieurs pages.

Une représentation sous forme de graphe est naturelle :

```text
NODE = repère structurel
EDGE = relation spatiale/topologique
ULISTAG = graphe + tokens relationnels + métadonnées de version
```

### 4.3 Tokens structurels candidats

À la manière des paires ancre-cible de Shazam, une primitive suffisamment stable peut jouer le rôle d'**ancre** et être associée à un ensemble borné de voisines.

Un token peut encoder, après quantification :

- type de l'ancre ;
- type de la cible ;
- delta X relatif ;
- delta Y relatif ;
- rapport de largeur ;
- rapport de hauteur ;
- relation topologique ;
- éventuellement classe textuelle stable.

Le token ne doit pas embarquer une donnée personnelle ou métier variable.

Cette proposition est une hypothèse de recherche : le choix exact des primitives, de la quantification et du fan-out doit être évalué expérimentalement.

## 5 — Règles de fabrication candidates

1. Lire le document **localement**.
2. Normaliser chaque page dans un espace géométrique commun, par exemple coordonnées relatives `[0,1]`.
3. Détecter les primitives disponibles avec les briques locales.
4. Éliminer ou masquer les données manifestement variables ou sensibles.
5. Sélectionner des ancres structurelles selon stabilité et discriminance.
6. Générer des relations locales dans un voisinage borné.
7. Produire des tokens structurels comparables.
8. Conserver en parallèle le graphe explicable permettant d'interpréter la comparaison.
9. Versionner le règlement de fabrication indépendamment des documents et profils.

## 6 — Comparaison candidate

La comparaison ne doit pas reposer sur un unique pourcentage global.

Pipeline candidat :

```text
ULISTAG observé
→ recherche de tokens communs
→ génération de candidats
→ correspondances de repères
→ test de cohérence spatiale
→ agrégation par page / zone
→ classement des modèles candidats
→ MATCH | AMBIGUOUS | UNKNOWN selon politique du consommateur
```

La cohérence spatiale peut être évaluée sous une transformation tolérée, par exemple :

- mise à l'échelle ;
- translation ;
- petites variations de positions ;
- variations locales de blocs.

Le consommateur reste responsable de sa politique de décision. ULISDOQ fournit conventions, références et preuves ; il n'impose pas une probabilité universelle.

## 7 — Versionnement et variantes

Distinguer :

- **version du schéma ULISTAG** : structure du format d'empreinte ;
- **version du règlement de fabrication** : algorithme et paramètres ;
- **version du TAG de référence** : évolution du modèle documentaire ;
- **version du profil d'extraction** : règles d'extraction ;
- **version du moteur / composant technique**.

Un changement d'année, logo ou bloc ne doit pas être automatiquement interprété comme un nouveau format. Il faut déterminer expérimentalement s'il s'agit :

- d'une variable ;
- d'une variante compatible ;
- d'une version de modèle ;
- d'une rupture de modèle.

## 8 — Confidentialité

L'ULISTAG est dérivé d'un document potentiellement privé. Il n'est **pas présumé anonyme par construction**.

Avant publication d'une empreinte :

- supprimer les valeurs variables identifiantes ;
- éviter les séquences textuelles personnelles ;
- quantifier suffisamment les coordonnées lorsque pertinent ;
- auditer les logos / codes / identifiants susceptibles de révéler une organisation ou un individu ;
- conserver la possibilité de ne publier que le TAG de référence construit sur des fixtures autorisées.

Le document privé et son ULISTAG local complet peuvent rester exclusivement chez le consommateur.

## 9 — RETEX GED-01

Le test `GED01_VISUAL_GRID_V0_1` a donné :

- 2 pages contre 2 pages ;
- géométries de pages compatibles ;
- similarité page 1 : 70,78 % ;
- similarité page 2 : 78,57 % ;
- moyenne : 74,68 % ;
- seuil initial : 78 % ;
- verdict initial : `NON_MATCH`.

Ce résultat ne démontre pas une différence de modèle. Il montre surtout qu'une métrique globale et un seuil arbitraire sont insuffisants pour une décision finale.

Le préfiltre visuel peut rester utile pour ordonner des candidats, mais ne doit pas remplacer l'analyse de relations structurelles.

Le premier essai invoice2data ayant comporté une erreur de transcription des expressions régulières, il n'est pas retenu comme preuve d'échec du profil.

## 10 — Protocole expérimental GED-01 candidat — collaboration avec CLAU/GED-RÉEL

GED-01 est un **cas réel porté par CLAU/GED-RÉEL et coordonné par CLAU/LIFECYCLE**. ULISDOQ fournit et fait évoluer les objets génériques utiles à l'expérience (profil candidat, conventions TAG/ULISTAG, règles de comparaison et de qualification), puis reçoit les RETEX et preuves partageables. Le document privé, les exécutions locales et les observations contenant des données personnelles restent dans le périmètre autorisé de CLAU/GED-RÉEL.

Cette séparation signifie que la feuille de route ci-dessous décrit les besoins expérimentaux d'ULISDOQ ; elle ne transfère pas le pilotage opérationnel du cas réel à ULISDOQ.

### P0 — Gros plan structurel

Sur le document réel local et la fixture GED-01 :

- lire avec le même composant et la même version ;
- produire les mêmes primitives ;
- normaliser les coordonnées ;
- comparer les caractéristiques candidates ;
- qualifier chaque caractéristique comme stable, variable ou incertaine.

### P1 — Deux ULISTAG selon un même règlement

A — ULISTAG local du document réel ;  
B — ULISTAG de la fixture expérimentale.

Comparer :

- primitives communes ;
- tokens relationnels communs ;
- cohérence spatiale ;
- zones divergentes ;
- rôle des données variables.

### P2 — Témoin négatif

Ajouter au moins un document de modèle différent, légalement utilisable et non sensible.

Le but n'est pas seulement d'obtenir un score élevé A↔B, mais également une séparation nette par rapport au témoin.

### P3 — Profil associé

Si le rapprochement structurel place correctement GED-01 parmi les candidats :

- résoudre vers `experiments/factures/GED-01/templates/fournisseur_exp_01.yml` ;
- exécuter l'extraction sur le document réel local ;
- vérifier les champs attendus ;
- qualifier séparément le profil et l'empreinte.

### P4 — Extension

Avant toute généralisation :

- plusieurs positifs indépendants ;
- variantes du modèle ;
- négatifs proches ;
- documents de même émetteur mais modèles différents si disponibles.

## 11 — Mesures à collecter

- rappel de candidats ;
- précision du top-k ;
- faux rapprochements ;
- faux rejets ;
- `UNKNOWN` et `AMBIGUOUS` ;
- stabilité des primitives ;
- stabilité des relations ;
- sensibilité au contenu variable ;
- tolérance à translation / échelle / petits déplacements ;
- coût CPU/RAM ;
- taille d'index ;
- reproductibilité par version ;
- explicabilité du rapprochement.

## 12 — Acquis, hypothèses et questions ouvertes

### Acquis

- L'utilisation de caractéristiques locales robustes et de relations entre caractéristiques est un principe éprouvé en audio fingerprinting.
- La similarité structurelle de layouts, la représentation par graphes et la combinaison texte + géométrie sont des domaines de recherche établis.
- Une métrique globale de pixels ne suffit pas à représenter la structure d'un document.
- Le corpus ULISDOQ existant distingue déjà signature observée, TAG, profil et moteur.

### Hypothèses ULISTAG à éprouver

- un petit nombre de primitives structurelles robustes peut suffire pour la découverte de candidats ;
- des tokens relationnels quantifiés peuvent permettre une indexation rapide ;
- la cohérence d'un ensemble de relations est plus discriminante qu'une somme de ressemblances isolées ;
- un graphe explicite peut fournir à la fois recherche et explicabilité.

### Questions ouvertes

- quelles primitives restent stables entre documents réellement distincts d'un même modèle ?
- quelle quantification géométrique maximise robustesse sans perdre la discriminance ?
- combien de relations par ancre sont nécessaires ?
- faut-il des tokens différents pour texte, géométrie et graphisme ?
- comment représenter proprement les documents multi-pages ?
- comment reconnaître les variantes compatibles sans fusionner des modèles voisins ?
- quelle part de la comparaison peut être réemployée depuis des briques existantes ?
- à partir de quel déficit mesuré un modèle appris devient-il justifié ?

## 13 — Feuille de route candidate

```text
R0  CLAU/GED-RÉEL
    Réutiliser la caractérisation structurelle locale déjà acquise.
    Compléter uniquement les éléments manquants au regard
    des critères attendus fournis par ULISDOQ.

R1  ULISDOQ
    Définir le schéma ULISTAG expérimental minimal.

R2  COLLABORATION
    Construire deux exemples synthétiques A/B de même structure
    avec des valeurs différentes, plus un témoin négatif
    de structure différente.
    Vérifier les invariants et les différences de l'empreinte.
    Aucun transfert du document privé.

R3  ULISDOQ
    Éprouver un comparateur déterministe explicable candidat.
    Documenter ce que sa mesure signifie et ses limites,
    sans assimiler automatiquement similarité et probabilité.

R4  ULISDOQ
    Établir la liaison :
    ULISTAG → profil candidat versionné → fournisseur_exp_01.

    Une correspondance propose un traitement ;
    elle ne prouve pas sa validité sur le document réel.

R5  CLAU/GED-RÉEL
    Exécuter et vérifier l'extraction localement.
    Retourner des preuves partageables et les écarts observés.

R6  COLLABORATION
    Éprouver la généralisation sur un petit corpus indépendant
    des exemples utilisés pour concevoir et régler le mécanisme.

R7  DÉCISION
    Poursuivre / simplifier / abandonner /
    introduire une brique plus avancée.
```

### Parallélisation admise

R5 peut avancer **en parallèle de R1 à R4** avec le profil canonique exact déjà disponible. L'extraction réelle GED-01 n'a pas à attendre l'existence d'un matcher général.

Le retour R5 qualifie l'exécution et la compatibilité du profil sur le cas observé ; il ne qualifie pas à lui seul ULISTAG ni la reconnaissance générale du modèle.

### Arbitrage continu

La décision de poursuivre, simplifier, abandonner ou changer de brique reste possible **après chaque étape**. R7 formalise la décision de synthèse ; il n'interdit pas d'arrêter plus tôt une piste dont l'utilité n'est pas démontrée.

Aucune étape n'autorise par elle-même une déclaration de technologie qualifiée ou de taux de reconnaissance généralisable.

## 14 — Première réalisation GED-01 v0.1

La première méthode effectivement élue et prototypée pour GED-01 est documentée dans :

`experiments/factures/GED-01/ulistag/ANCHOR_GRAPH_V0_1.md`

Choix v0.1 :

```text
ANCRES_TEXTUELLES_STABLES
→ COORDONNEES_NORMALISEES
→ GRAPHE_DE_RELATIONS_GEOMETRIQUES
→ COMPARAISON_DETERMINISTE_EXPLICABLE
→ MATCH_CANDIDATE | UNKNOWN
→ PROFIL_STRUCTUREL_ASSOCIE
→ EXTRACTION_RELATIVE_AUX_ANCRES
```

Ce choix ne remplace pas l'état de l'art général. Il constitue la solution minimale retenue pour le premier cas réel, jusqu'à preuve de son insuffisance.

Le profil d'extraction structurel v0.1 est distinct du profil `invoice2data` historique et conserve la géométrie afin d'éviter les erreurs dues à l'aplatissement du texte.


### RETEX PCIA — PASS_CANDIDATE

CLAU/GED-RÉEL a exécuté le candidat v0.1 sur PCIA avec Python 3.12.3 et pdfplumber 0.11.10, en références épinglées.

Résultat :

```text
MATCH_CANDIDATE
page_count=2
node_ratio=1.0
edge_ratio=1.0
missing_nodes=NONE
failed_edges=NONE

EXTRACTED_UNVERIFIED
invoice_number=EXTRACTED
date=EXTRACTED
amount=EXTRACTED

qualification=NONE
```

Aucune valeur privée n'a été retournée. Ce résultat valide l'**exécutabilité du candidat sur sa source de conception**, pas sa généralisation ni la correction des valeurs extraites.

RETEX détaillé : [GED01_ULISTAG_V0_1_PCIA_EXECUTION_001](../experiments/factures/GED-01/docs/RETEX_ULISTAG_V0_1_PCIA_EXECUTION_001.md).

La prochaine étape prioritaire devient l'épreuve **A/B synthétiques + témoin négatif** selon le même règlement, puis un corpus indépendant.

## 15 — Références

- Avery Li-Chun Wang, *An Industrial-Strength Audio Search Algorithm*, ISMIR 2003.
- Jianying Hu, Ramanujan Kashi, Gordon Wilfong, *Comparison and Classification of Documents Based on Layout Similarity*, Information Retrieval.
- *Structural similarity for document image classification and retrieval*, Pattern Recognition Letters, 2014.
- Reza Azmi et al., *LGL-DIR: Layout graph for layout based document image retrieval*, 2010.
- Akshay Gadi Patil et al., *LayoutGMN: Neural Graph Matching for Structural Layout Similarity*, CVPR 2021.
- Yiheng Xu et al., *LayoutLM: Pre-training of Text and Layout for Document Image Understanding*, 2019/2020.
- Yang Xu et al., *LayoutLMv2: Multi-modal Pre-training for Visually-Rich Document Understanding*, 2020/2021.
- Yufan Chen et al., *Graph-based Document Structure Analysis*, ICLR 2025.
- Rubel Biswas, Pablo Blanco-Medina, *State of the Art: Image Hashing*, 2021.
