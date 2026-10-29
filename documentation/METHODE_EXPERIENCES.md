# GED-RÉEL — Invariant transversal de représentativité consommateur

**Autorité :** Jean  
**Méthode :** CLAU_METHODE_V2_BETA_5  
**Statut :** INVARIANT_EXPERIMENTAL_TRANSVERSAL  
**Périmètre :** GED-01 à GED-70 et expériences GED ultérieures

## Invariant

Toute expérience GED doit définir comme cible une **entrée documentaire plausible d'un consommateur réel**, et non se limiter au document numérique natif idéal. La reconnaissance d'identité documentaire doit pouvoir être éprouvée face aux dégradations de numérisation : faible résolution, absence de couche texte, compression, bruit, rotation, contraste imparfait, rognage et variations de pagination pertinentes.

**Reconnaissance ≠ extraction ≠ validation du contenu.** L'identification du type, du modèle, de la version ou du millésime doit être testée séparément de l'extraction de valeurs et de leur vérification.

## Conséquences pour chaque GED

1. Documenter les conditions d'entrée réelles visées et leurs limites ; ne pas présumer que tout document est scanné, mais inclure un chemin de dégradation pertinent à la famille.
2. Conserver la provenance des sources : authentique, dérivé, synthétique. Les scans simulés ne valent pas preuve sur scans indépendants.
3. Inclure ou planifier un témoin négatif et des cas ambigus, avec possibilité de décision `UNKNOWN`/`AMBIGUOUS` lorsque les preuves sont insuffisantes.
4. Distinguer `NATIVE_SOURCE_PASS`, `DEGRADED_INPUT_PASS` et `REAL_WORLD_QUALIFIED`. Aucun passage automatique d'un statut à l'autre.
5. Définir le besoin de corpus indépendant, les métriques, les faux positifs et les faux rejets avant toute revendication de qualification.
6. Préserver la confidentialité des documents consommateurs ; aucun transfert ou publication de données privées sans base et autorisation appropriées.

## Articulation avec la stratégie GED-02 à GED-70

Cet invariant est **une exigence de conception et de preuve**, non un verrou imposant une qualification complète de chaque cas avant d'avancer. En phase 1, chaque GED peut conclure par un RETEX et une dette de qualification explicite. Les cas disposant de variantes indépendantes pertinentes seront approfondis en phase 2.

**GED-01 :** `MATCH_CANDIDATE` sur source de conception ; qualification consommateur non acquise.  
**GED-02 :** `PASS_R0` sur 2044 2025 officielle native ; reconnaissance d'un scan consommateur basse résolution non acquise.

## Règle d'acceptation

**FORBIDDEN:** `NATIVE_SOURCE_PASS => REAL_WORLD_QUALIFIED`.

**NEXT_ACTOR:** ULISDOQ — intégrer l'invariant dans les contrats de cas et la feuille de route ; CLAU/GED-RÉEL — l'appliquer à chaque nouveau GED.
