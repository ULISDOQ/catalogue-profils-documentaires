# GED-02 — Formulaire fiscal 2044, millésime 2025 (DGFiP)

**Statut :** R0_PASS_PCIA — QUALIFICATION_SCAN_BASSE_RESOLUTION_A_REALISER  
**Autorité :** Jean — CLAU_METHODE_V2_BETA_5  
**Famille :** formulaire administratif / déclaration fiscale structurée  
**Nature :** document public authentique vierge ; aucune déclaration personnelle

## Source officielle vérifiée

- Organisme : Direction générale des Finances publiques (DGFiP)
- Formulaire : n° 2044, déclaration des revenus fonciers
- Millésime : **2025**, Cerfa **10334*29**, publication 16 avril 2025
- Exercice fiscal indiqué dans le PDF : **revenus fonciers 2024** (attention : millésime 2025 ≠ revenus 2025)
- PDF original : https://www.impots.gouv.fr/sites/default/files/formulaires/2044/2025/2044_5132.pdf
- Page de référence : https://www.impots.gouv.fr/formulaire/2044/declaration-des-revenus-fonciers
- Pages PDF : 4 (observation de la source officielle via consultation)
- Source téléchargée sur PCIA : **OUI, R0 PASS, 2026-10-20**
- SHA256 du PDF R0 : `6c9798559408deef0646cf93cbf9f933c7da1cbd404ac2129e54d52fc3369e9b`
- Droit de redistribution : **A VERIFIER AVANT REHEBERGEMENT** ; conserver ici seulement URL et métadonnées.

## Pourquoi GED-02

Contraste délibéré avec GED-01 (facture télécom). Document à grille, rubriques numérotées, cases, colonnes répétées par immeuble, reports interpages, totaux et calculs. Le formulaire vierge permet de tester la reconnaissance de structure et des champs **sans prétendre extraire des valeurs réelles**.

## Repères observables dans le PDF officiel

- Page 1 : sections 100, 110, 120 ; lignes 111 à 115.
- Pages 2 et 3 : propriétés rurales et urbaines ; lignes 211 à 263 ; répétition par immeuble.
- Page 4 : résultat 420 ; répartition 430 à 442 ; déficits 450 ; travaux 400 ; intérêts d'emprunt 410 ; vente/cessation 460.

Ces repères sont des hypothèses de caractérisation à vérifier par le lecteur PDF local, pas encore des ancres ULISTAG qualifiées.

## Première expérience bornée GED-02 / R0

1. Acquérir sur PCIA le PDF **exact** via l'URL officielle, sans remplir ni modifier le formulaire.
2. Vérifier statut HTTP, type PDF, taille, SHA256, nombre de pages et versions du lecteur.
3. Observer couche texte, coordonnées, annotations/champs AcroForm éventuels, tableaux et lignes de report ; ne pas inventer leur présence.
4. Produire une carte structurelle minimisée : numéros de rubriques par page, types de zones, répétitions, présence/absence de champs interactifs.
5. Retourner seulement métadonnées, dénombrements, statuts et difficultés techniques.
6. Ne pas générer de fausses données fiscales à ce stade ; des variantes synthétiques pourront suivre, explicitement étiquetées.
7. Aucune création de profil ULISTAG ni qualification automatique lors de R0.

## Résultat attendu

`SOURCE_FETCH=PASS|FAIL`; `SHA256`; `PAGE_COUNT`; `TEXT_LAYER`; `ACROFORM_FIELDS_COUNT`; `STRUCTURE_OBSERVED`; `LIMITS`; `PRIVATE_VALUES=NONE`.

## Valeur de recherche pour ULISDOQ

Tester si une même famille de méthodes permet d'identifier les rubriques, la structure des colonnes et les renvois entre pages. Différencier **reconnaissance du formulaire**, **localisation des cases**, **extraction de valeurs remplies** et **vérification des règles fiscales**. Les trois dernières ne sont pas démontrées sur le formulaire vierge.

## Suites

- R1 : comparer millésimes 2024/2025/2026 en tant que documents authentiques indépendants et mesurer les changements de structure.
- R2 : proposer une variante remplie **strictement synthétique**, jamais assimilée à une déclaration authentique.
- R3 : capitaliser les méthodes transverses pour les futurs cas GED.

**NEXT_ACTOR : CLAU/GED-RÉEL — acquisition et observation PCIA R0.**


## Exigence de qualification GED-02 — scan consommateur basse résolution

**Décision de Jean (2026-10-20) :** GED-02 doit viser la reconnaissance d'une 2044 millésime 2025 numérisée, même dégradée, telle qu'un consommateur réel pourrait la fournir. Le PASS_R0 sur PDF natif ne qualifie pas cette capacité.

### Contrat de reconnaissance à qualifier

- Entrées : image/PDF raster de pages scannées, sans couche texte ni AcroForm utilisable ; résolution basse, bruit, compression, rotation, pages multiples ; données personnelles interdites dans les fixtures publiques.
- Sorties : `MATCH_CANDIDATE` / `UNKNOWN` / `AMBIGUOUS`, identité 2044, millésime 2025, pages détectées, éléments structurels de preuve, limites et provenance de la méthode.
- Ne jamais présenter un score comme probabilité sans calibration ; ne pas confondre reconnaissance, extraction des données fiscales et validation fiscale.
- Une page absente, illisible ou une version indiscernable doit conduire à une décision explicitement partielle, ambiguë ou inconnue, et non à une qualification implicite.

### Protocole progressif

1. **R1 — Corpus contrôlé :** partir du PDF officiel et générer des scans simulés à plusieurs résolutions (dont 100/150/200 dpi), niveaux JPEG, bruit, inclinaison, contraste, rognage ; documenter paramètres et empreintes. Ce sont des **dérivés synthétiques**, pas des scans consommateurs authentiques.
2. **R2 — Baseline :** essayer les lecteurs OCR et/ou empreintes de layout avec preuves d'ancres, géométrie et repères de pages. Consigner les échecs sans modifier le candidat pendant la passe.
3. **R3 — Témoins négatifs :** autres formulaires fiscaux, autres millésimes de 2044, pages permutées/manquantes et documents voisins ; vérifier faux positifs et confusion de millésime.
4. **R4 — Validation indépendante :** scans réellement produits avec plusieurs équipements, paramètres et opérateurs, puis si possible échantillons de consommateurs légalement obtenus, minimisés et autorisés. Garder les échantillons d'évaluation séparés des documents de conception.
5. **R5 — Qualification bornée :** publier une matrice de tests, taux de reconnaissance/faux positifs/faux rejets, conditions d'utilisation, limites, décision humaine et statut de maturité. Aucun seuil numérique de qualification n'est fixé sans protocole et corpus représentatifs.

### Frontières

Ne pas publier de déclaration fiscale remplie, données fiscales privées, OCR brut de consommateurs ou scans non autorisés. La qualification vise d'abord **l'identité du formulaire et du millésime**, non la justesse des montants déclarés. Les scans issus du PDF officiel sont des essais de robustesse et ne suffisent pas seuls à revendiquer un fonctionnement en conditions réelles.

**NEXT_ACTION :** préparer R1 et R3 comme lots reproductibles, puis définir la baseline de reconnaissance avec ULISDOQ avant toute affirmation de qualification.
