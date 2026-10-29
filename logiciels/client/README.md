# Client ULISDOQ

Le client ULISDOQ est une **capacité transverse du projet**, indépendante d'une expérience particulière. Il exécute localement des opérations documentaires à partir de ressources du catalogue ; les expériences sous `experiences/` l'utilisent comme cas d'épreuve.

## Extraction locale avec invoice2data

`extract.py` charge explicitement un répertoire de profils YAML et appelle l'API Python publique d'[invoice2data](https://invoice2data.readthedocs.io/stable/usage.html). Aucun document n'est transmis à ULISDOQ.

Pour un déploiement reproductible, ne pas installer `invoice2data` globalement. Utiliser le profil complet Ubuntu ou l'environnement isolé `invoice2data` qu'il crée.

Exemple avec GED-01 après installation du profil complet :

```bash
"$HOME/.local/share/ulisdoq/complete-v0_1/venvs/invoice2data/bin/python" logiciels/client/extract.py \
  experiences/factures/GED-01/specimens/Fournisseur-EXP-01_document_experimental.pdf \
  --templates experiences/factures/GED-01/modeles \
  --reader tesseract > resultat.json
```

Le résultat est un JSON avec `status`, `source_sha256`, `engine`, `reader` et `data` si extraction. Codes retour : 0 extraction non vérifiée ; 1 aucun profil reconnu ; 2 erreur. **Une extraction n'est jamais une qualification.**

## ULISTAG

La reconnaissance structurelle possède désormais son propre espace cœur dans [`logiciels/ULISTAG/`](../ULISTAG/README.md). Le client ULISDOQ reste transverse et ne porte plus l'implémentation interne des matchers.

Le premier matcher candidat est :

`logiciels/ULISTAG/matchers/anchor_graph/ulistag_v0.py`

Les références et preuves propres à GED-01 restent sous `experiences/factures/GED-01/ulistag/`.

## TAG candidat

`tag_candidate.py` prépare localement un descripteur de TAG candidat à partir d'indices explicitement fournis. `test_tag_candidate.py` vérifie ce composant. Son protocole est documenté dans [protocole TAG candidat](documentation/PROTOCOLE_TAG_CANDIDAT.md).

## Reconnaissance de format

Le manque fonctionnel identifié relève de **HORIZON-FORMAT-001** : comparer une signature observée aux TAGs du catalogue, retourner une correspondance qualifiée, ambiguë ou inconnue, puis résoudre la liaison **TAG → profil d'extraction**.

## Positionnement

Le client n'appartient ni à GED-01, ni à GED-02, ni à une maturité particulière du catalogue. Une expérience peut fournir ses fixtures, profils, paramètres et critères de preuve ; le client reste générique et réutilisable.


## Déploiement reproductible

Le contrat de déploiement du client complet est documenté dans [profil complet Ubuntu](../deploiement/ubuntu/complete-v0_1/README.md).

Le profil sépare actuellement :

```text
core
anchor_graph
visual_keypoints
invoice2data
semantic_validation
```

afin d'éviter les conflits de dépendances. Tesseract et ses données linguistiques FR/EN sont des prérequis système du profil Ubuntu complet.
