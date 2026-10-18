# TAG candidat — protocole minimal

**Statut : démonstrateur local, non moteur de reconnaissance.**

L'éditeur `client/tag_candidate.py` produit un objet JSON versionné à partir d'indices **saisis explicitement** et d'une géométrie optionnelle. Il ne lit pas de PDF, ne réalise pas d'OCR et ne contacte aucun serveur. Son empreinte SHA-256 garantit la stabilité du descripteur canonisé, **pas la reconnaissance d'un document**.

Exemple :

```bash
python client/tag_candidate.py \
  --family tax_declaration_form \
  --marker '2044' --marker 'revenus fonciers' \
  --output tag_candidate_2044.json
```

La prochaine fonction à réaliser est **la consultation d'un index local ULISDOQ versionné**, renvoyant MATCH, AMBIGUOUS ou UNKNOWN sur des critères de similarité évalués. Une simple égalité de hachage n'est pas une preuve de reconnaissance robuste.

Aucune donnée personnelle, montant, identifiant de contribuable ou document brut ne doit être publié dans un TAG. Le profil 2044 est un candidat conceptuel, non un modèle officiel validé.

Critères de qualification : corpus autorisé et indépendant, négatifs, exactitude des versions, faux positifs, ambiguïtés, compatibilité du moteur d'extraction, preuve reproductible et revue.
