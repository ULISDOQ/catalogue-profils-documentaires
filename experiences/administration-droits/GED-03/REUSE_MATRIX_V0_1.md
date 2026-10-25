# GED-03 — Matrice de réemploi GED-core

**Référence : GED03-REUSE-MATRIX-001**  
**Statut : préparation, non exécutée**

| Élément | GED-01 | GED-02 | GED-03 décision proposée | Motif |
|---|---|---|---|---|
| Méthode GED-N phase 1 | oui | oui | REUSE | contrat transversal |
| Registre de profils | non/partiel | oui | ADAPT/REUSE | identité et version du profil |
| TAG candidat | oui | oui | OPTIONAL | .eml possède déjà une structure de conteneur forte |
| ULISTAG anchor_graph | oui | non | DO_NOT_USE | pas de besoin observé |
| ULISTAG visual_keypoints | non | oui | DO_NOT_USE | pas de rendu visuel nécessaire |
| OCR | selon moteur | oui | DO_NOT_USE | texte et MIME natifs |
| invoice2data | oui | non | DO_NOT_USE | domaine facture uniquement |
| profile_ocr_extract | non | oui | DO_NOT_USE | binding géométrique inutile |
| schéma JSON | oui | oui | REUSE_PATTERN | sortie normalisée vérifiable |
| statuts explicites | oui | oui | REUSE | refus/ambiguïté nécessaires |
| hashes/version/preuves | oui | oui | REUSE | reconstructibilité |
| Python stdlib email | non | non | EVALUATE | primitive candidate native |
| grammaire métier | faible | DGFIP candidate | NONE_INITIAL | pas d'interprétation métier du contenu |

## Hypothèse de réemploi

Le gain attendu de GED-core n'est pas le nombre maximal de composants réutilisés.

La bonne décision est celle qui minimise la chaîne tout en satisfaisant le contrat :

```text
EML
→ parser natif
→ normalisation
→ validation schema
→ preuve
```

Toute introduction d'OCR, visual-keypoints ou LLM sans besoin observé constitue un échec du principe de proportionnalité.
