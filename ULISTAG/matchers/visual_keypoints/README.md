# Visual keypoints — matcher candidat v0.1

Ce matcher ULISTAG cœur reconnaît une structure documentaire à partir de **points visuels locaux** détectés sur les pages rendues.

Chaîne :

```text
PDF
→ rendu niveaux de gris
→ points ORB + descripteurs
→ appariement Hamming
→ filtre de ratio
→ cohérence géométrique par homographie RANSAC
→ décision page
→ décision document
```

Il a été introduit par GED-02 parce que le PDF officiel 2044 possède une couche texte exploitable alors que les spécimens synthétiques peuvent être image-only. Le matcher travaille donc sur une représentation commune : la page rendue.

Ce composant est **générique** : aucun mot « 2044 », aucune zone fiscale et aucune valeur métier ne sont codés dans l'algorithme.

Dépendances candidates : Python 3, PyMuPDF, OpenCV, NumPy.

Statut : `CANDIDATE_UNQUALIFIED`.
