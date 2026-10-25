# GED-02 — ULISTAG layout-density v0.1

**Référence : ULISTAG-GED02-LAYOUT-DENSITY-001**  
**Statut : CANDIDAT PHASE 1 — NON QUALIFIÉ**  
**Objet : reconnaissance candidate du formulaire 2044 millésime étudié**

## Corpus expérimental

Le corpus fourni à ULISDOQ contient :

- huit spécimens synthétiques positifs S01 à S08, dérivés du même modèle 2044 ;
- un témoin négatif synthétique N01, volontairement fiscal et visuellement proche dans son vocabulaire général.

Les PDF sont des documents image-only dans l'environnement d'étude : aucune couche texte exploitable n'a été observée.

Les documents sources ne sont pas copiés dans Git. Seuls la méthode, le descripteur dérivé et les résultats minimisés sont capitalisés.

## Question de phase 1

Peut-on obtenir un TAG candidat simple, sans OCR ni compréhension sémantique, qui rapproche les huit variantes 2044 et rejette le témoin négatif ?

## Méthode retenue

La méthode v0.1 utilise une **empreinte de densité de mise en page multi-pages** :

```text
PDF
→ rendu image normalisé
→ niveaux de gris
→ rognage uniforme des marges
→ autocontraste
→ densité d'encre
→ grille 16 × 24 par page
→ concaténation des quatre pages
→ normalisation L2
→ similarité cosinus avec la référence
```

Aucun OCR n'est requis.

Cette méthode ne cherche pas à comprendre les champs ni le sens du formulaire. Elle mesure seulement une compatibilité grossière de structure graphique.

## Construction de la référence

Jeu de conception :

```text
S01 S02 S03 S04 S05
```

Le vecteur de référence est la moyenne des cinq descripteurs, puis normalisé L2.

Le témoin N01 a participé au choix du seuil expérimental. Il ne constitue donc **pas** un négatif indépendant de qualification.

Validation positive conservée hors construction de la référence :

```text
S06 S07 S08
```

## Paramètres v0.1

```text
page_count = 4
render_dpi = 110
crop_fraction = 0.03
grid = 16 × 24 par page
similarity = cosine
candidate_threshold = 0.85
```

Le score est une similarité structurelle selon ce descripteur. Ce n'est pas une probabilité.

## Résultat

Les huit positifs obtiennent `MATCH_CANDIDATE`.

Le témoin négatif obtient `UNKNOWN`.

Les trois positifs non utilisés dans la construction de la référence obtiennent également `MATCH_CANDIDATE`.

Voir [RESULTS_V0_1.md](RESULTS_V0_1.md).

## Pourquoi cette méthode est intéressante en phase 1

- très peu de primitives ;
- aucun OCR ;
- calcul déterministe ;
- coût faible ;
- indépendance vis-à-vis des valeurs remplies ;
- descripteur compact et indexable ;
- facilement remplaçable si d'autres cas montrent ses limites.

Elle n'est **pas promue dans le cœur ULISTAG** à ce stade : un seul GED-N a démontré son intérêt.

## Limites et dettes

- corpus synthétique uniquement ;
- un seul négatif, utilisé pendant la conception ;
- même nombre de pages exigé ;
- aucune validation sur scan dégradé, rotation, recadrage ou autre millésime ;
- aucune discrimination démontrée face à 2044-SPE ou autres formulaires fiscaux réels très proches ;
- le seuil 0.85 est expérimental ;
- aucune qualification de production.

La phase 1 s'arrête volontairement ici si la méthode suffit au cas. Les perfectionnements sont matière de phase 2 ou d'un futur cas qui mettra cette méthode en défaut.
