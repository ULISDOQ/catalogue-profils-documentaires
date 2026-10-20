# GED-02 — Résultats ULISTAG layout-density v0.1

**Statut : PASS_CANDIDATE — QUALIFICATION=NONE**

Référence construite avec S01-S05. Seuil expérimental : `0.85`.

| Spécimen | Rôle | Similarité | Résultat |
|---|---|---:|---|
| S01 | conception positive | 0.965026 | MATCH_CANDIDATE |
| S02 | conception positive | 0.983651 | MATCH_CANDIDATE |
| S03 | conception positive | 0.961431 | MATCH_CANDIDATE |
| S04 | conception positive | 0.978475 | MATCH_CANDIDATE |
| S05 | conception positive | 0.984385 | MATCH_CANDIDATE |
| S06 | validation positive | 0.955646 | MATCH_CANDIDATE |
| S07 | validation positive | 0.920930 | MATCH_CANDIDATE |
| S08 | validation positive | 0.965773 | MATCH_CANDIDATE |
| N01 | négatif de conception | 0.720306 | UNKNOWN |

## Lecture

Le plus faible positif observé reste à `0.920930`, tandis que le négatif est à `0.720306`.

Cela montre une séparation nette **sur ce corpus**, suffisante pour retenir la méthode comme candidat de phase 1.

Cela ne permet pas d'estimer un taux de faux positifs ou faux négatifs généralisable. N01 ayant participé au réglage, la séparation négative n'est pas une validation indépendante.

## Robustesse exploratoire du niveau de grille

Une vérification exploratoire sur plusieurs granularités de grille a conservé une séparation entre les positifs de validation et N01. Cette observation soutient le principe de la méthode, mais ne remplace pas une qualification indépendante.

## Décision

```text
GED02_ULISTAG_PHASE1=PASS_CANDIDATE
METHOD=LAYOUT_DENSITY_V0_1
QUALIFICATION=NONE
PROMOTION_TO_ULISTAG_CORE=NO
NEXT=CAPITALIZE_AND_CONTINUE_HORIZONTAL_EXPLORATION
```
