# Étude de faisabilité — Couvrir 80 % de la paperasserie de 1 000 organisations

**Référence : FEASIBILITY-PROFILE-COVERAGE-001**  
**Statut : première estimation de dimensionnement — à vérifier expérimentalement**  
**Objet : estimer l'ordre de grandeur du nombre de profils documentaires qualifiés nécessaires pour couvrir environ 80 % des documents courants rencontrés par 1 000 organisations.**

## Question

ULISDOQ vise la mutualisation de profils documentaires réutilisables. La question de faisabilité n'est donc pas :

```text
1 organisation = 1 profil
```

mais :

```text
combien de modèles documentaires distincts
faut-il qualifier
pour couvrir une part importante
du volume documentaire réellement rencontré ?
```

## Première estimation

À ce stade, sans corpus statistique représentatif de 1 000 organisations, l'ordre de grandeur candidat est :

```text
500 profils qualifiés
→ couverture déjà significative mais encore lacunaire

≈ 1 000 profils qualifiés
→ hypothèse de travail crédible pour viser environ 80 %

2 000 profils qualifiés
→ marge plus importante pour les variantes,
  millésimes et secteurs professionnels
```

La fourchette de faisabilité initiale retenue est donc **500 à 2 000 profils**, avec **environ 1 000 profils** comme hypothèse centrale de travail.

Cette valeur n'est ni une cible normative, ni une prévision démontrée.

## Pourquoi le nombre de profils ne suit pas le nombre d'organisations

De nombreuses organisations reçoivent les mêmes familles et modèles de documents :

- factures de grands opérateurs et fournisseurs ;
- documents fiscaux et administratifs nationaux ;
- relevés et documents bancaires ;
- assurances, mutuelles et protection sociale ;
- transporteurs, fournisseurs nationaux et services récurrents.

La mutualisation peut donc être importante.

Inversement, une seule organisation émettrice peut produire plusieurs modèles documentaires :

```text
une organisation
├── modèle A
├── modèle B
├── variante professionnelle
├── variante grand public
└── millésimes ou ruptures de modèle
```

Le nombre d'organisations n'est donc ni le nombre de formats ni le nombre de profils.

## Décomposition indicative

| Domaine documentaire | Ordre de grandeur initial |
|---|---:|
| Documents administratifs et publics fréquents | 100–250 |
| Factures de grands fournisseurs, énergie, télécoms et opérateurs | 150–300 |
| Banque, assurance, mutuelle et protection sociale | 100–250 |
| Achats et fournisseurs professionnels fréquents | 150–400 |
| Logement, véhicules et services récurrents | 50–150 |
| Variantes importantes et millésimes nécessaires | +200–600 |

Ces intervalles servent uniquement à tester la plausibilité de l'ordre de grandeur. Ils se recouvrent partiellement et ne doivent pas être additionnés comme une comptabilité exacte.

## Hypothèse de distribution

La couverture documentaire devrait vraisemblablement suivre une distribution très asymétrique :

```text
petit noyau de profils très fréquents
→ forte part du volume

profils supplémentaires
→ gains de couverture décroissants

longue traîne
→ nombreux modèles rares
```

ULISDOQ doit donc privilégier la qualification des profils selon leur **gain réel de couverture**, plutôt que chercher à maximiser le nombre brut de profils présents dans le catalogue.

## Indicateur principal proposé

L'indicateur pertinent n'est pas :

> nombre total de profils dans le dépôt

mais :

> **taux de documents observés pouvant être associés à un profil qualifié dans le périmètre considéré**

Mesures complémentaires utiles :

- part de documents `MATCH` ;
- part `AMBIGUOUS` ;
- part `UNKNOWN` ;
- couverture par famille documentaire ;
- couverture par organisation ;
- nombre de profils nécessaires pour atteindre 50 %, 70 %, 80 %, 90 % ;
- fréquence de réutilisation d'un même profil entre organisations ;
- coût de qualification et de maintenance par profil ;
- impact des variantes et millésimes.

## Méthode de validation proposée

La faisabilité devra être vérifiée sur un corpus représentatif et autorisé :

```text
échantillon d'organisations
→ inventaire des documents entrants
→ regroupement par modèles documentaires
→ fréquence de chaque modèle
→ classement décroissant
→ qualification progressive des profils
→ courbe profils qualifiés / couverture réelle
```

La mesure doit porter sur le **volume documentaire observé**, et pas uniquement sur la diversité des émetteurs.

## Critère de décision

L'hypothèse « environ 1 000 profils pour environ 80 % de couverture sur 1 000 organisations » sera :

- **CONFIRMÉE** si les mesures convergent vers cet ordre de grandeur ;
- **RÉVISÉE** si le corpus révèle une mutualisation ou une fragmentation sensiblement différente ;
- **ABANDONNÉE** si la notion même de profil commun ne permet pas d'obtenir une couverture économiquement exploitable.

## Conclusion provisoire

La première estimation ne révèle pas d'obstacle d'échelle évident.

Une cible de l'ordre du millier de profils qualifiés paraît compatible avec une stratégie de catalogue mutualisé, à condition que :

1. les profils correspondent à des **modèles documentaires réutilisables**, et non aux organisations elles-mêmes ;
2. les modèles les plus fréquents soient qualifiés en priorité ;
3. les variantes et millésimes soient traités comme des objets versionnés lorsque nécessaire ;
4. la progression soit pilotée par la **couverture documentaire mesurée**.

La prochaine étape n'est donc pas d'accumuler arbitrairement des profils, mais de construire une première **courbe empirique de couverture**.
