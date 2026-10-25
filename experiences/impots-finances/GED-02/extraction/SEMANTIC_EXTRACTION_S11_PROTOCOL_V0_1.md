# GED-02 — Protocole S11 : qualification de profil et extraction sémantique

**Référence : GED02-S11-PCIA-PROFILE-AND-SEMANTIC-EXTRACTION-001**  
**Statut : protocole candidat de phase 1**  
**Qualification : NONE avant exécution PCIA**

## Objet

Éprouver sur PCIA un scan réaliste du formulaire 2044 2025 déjà identifié comme `GED02-S11_2044_2025_SYNTHETIC_COMPLETE_SCAN_GRAY.pdf`.

L'épreuve sépare strictement :

1. reconnaissance du profil documentaire ;
2. qualification de la méthode applicable ;
3. lecture OCR / manuscrite ;
4. extraction sémantique ;
5. comparaison aux valeurs synthétiques de référence.

Le document S11 n'est pas utilisé pour recalibrer ULISTAG avant le premier passage.

## Références immuables à vérifier

- profil : `profiles/fr_formulaire_2044_candidate.json`
- manifest ULISTAG : `../ulistag/reference_visual_v0_1_manifest.json`
- matcher cœur : `../../../..//ULISTAG/matchers/visual_keypoints/ulistag_visual_keypoints_v0.py`
- protocole ULISTAG GED-02 : `../ulistag/PHASE1_2044_VISUAL_KEYPOINTS_V0_1.md`

Les identités exactes doivent être relevées sur PCIA avant exécution.

## Gate A — reconnaissance du profil

Exécuter le matcher ULISTAG existant, sans recalibration ni changement de seuil.

Décision :

- `MATCH_CANDIDATE` : le scan est compatible avec le profil documentaire candidat 2044 selon la méthode actuelle ;
- `UNKNOWN` : limite de robustesse observée ; ne pas forcer le match ;
- toute erreur d'exécution est distincte d'un échec de reconnaissance.

Un succès renforce les preuves de phase 1 mais ne transforme pas le profil en profil de production qualifié.

## Gate B — qualification de la méthode d'extraction

La méthode d'extraction candidate doit être exécutée localement sur PCIA.

Ordre de préférence :

```text
page scannée
→ prétraitement minimal si nécessaire
→ OCR imprimé / manuscrit disponible localement
→ détection des champs
→ association identifiant officiel + libellé officiel
→ normalisation contrôlée
→ JSON sémantique
→ comparaison au ground truth synthétique
```

L'OCR n'est qu'un lecteur. Il ne définit ni l'identité du champ ni sa sémantique.

## Contrat du JSON sémantique

Chaque champ retourné conserve au minimum :

```json
{
  "official_id": "<identifiant tel qu'imprimé sur le formulaire, si présent>",
  "official_label": "<libellé officiel observé>",
  "status": "VALUE|EMPTY|NOT_APPLICABLE|UNREADABLE|AMBIGUOUS",
  "value": "<valeur normalisée ou null>",
  "raw_observation": "<optionnel ; local uniquement si sensible>",
  "page": 1,
  "evidence": {
    "reader": "<moteur/version>",
    "confidence": "<si le moteur en fournit une ; non assimilée à une probabilité de vérité>"
  }
}
```

### Sémantique des statuts

- `VALUE` : une valeur est effectivement présente et lue ;
- `EMPTY` : champ applicable mais laissé vide ;
- `NOT_APPLICABLE` : champ explicitement non applicable selon le spécimen / la structure ;
- `UNREADABLE` : une valeur est présente mais ne peut pas être lue de façon fiable ;
- `AMBIGUOUS` : plusieurs lectures ou rattachements restent plausibles.

`EMPTY`, `NOT_APPLICABLE` et `UNREADABLE` ne doivent jamais être fusionnés.

## Ground truth

Le ground truth synthétique reste séparé du résultat extrait.

La comparaison se fait champ par champ avec au minimum :

```text
CORRECT
INCORRECT
NOT_FOUND
STATUS_ERROR
AMBIGUOUS
```

Aucune correction manuelle silencieuse n'est admise dans le JSON extrait.

## Critères phase 1

### PROFILE_PASS

`MATCH_CANDIDATE` sans recalibration.

### METHOD_PASS

La chaîne d'extraction est reproductible sur PCIA, les versions sont connues, les identifiants/libellés DGFIP sont conservés et aucun champ n'est inventé.

### FUNCTIONAL_PASS

Tous les champs déclarés critiques pour cette passe correspondent au ground truth synthétique.

### PARTIAL

Le profil est reconnu mais une partie des champs est incorrecte, non lue ou ambiguë.

### FAIL

Échec de reconnaissance, erreur de méthode, valeur inventée ou perte de sémantique empêchant l'évaluation.

## Portée

Cette épreuve est un test de phase 1. Elle ne qualifie pas encore :

- tous les scans de formulaires 2044 ;
- tous les manuscrits ;
- d'autres millésimes ;
- la totalité des champs du formulaire ;
- un moteur OCR pour un usage général.

Les résultats doivent nourrir la phase 2, sans bloquer la progression vers GED-03.
