# Client ULISDOQ

Le client ULISDOQ est une **capacité transverse du projet**, indépendante d'une expérience particulière. Il exécute localement des opérations documentaires à partir de ressources du catalogue ; les expériences sous `experiments/` l'utilisent comme cas d'épreuve.

## Extraction locale avec invoice2data

`extract.py` charge explicitement un répertoire de profils YAML et appelle l'API Python publique d'[invoice2data](https://invoice2data.readthedocs.io/stable/usage.html). Aucun document n'est transmis à ULISDOQ.

Prérequis : Python 3, `invoice2data` et, selon le document, un moteur OCR local.

Exemple avec GED-01, depuis la racine du dépôt :

```bash
python -m pip install invoice2data
python client/extract.py \
  experiments/factures/GED-01/fixtures/Fournisseur-EXP-01_document_experimental.pdf \
  --templates experiments/factures/GED-01/templates \
  --reader tesseract > resultat.json
```

Le résultat est un JSON avec `status`, `source_sha256`, `engine`, `reader` et `data` si extraction. Codes retour : 0 extraction non vérifiée ; 1 aucun profil reconnu ; 2 erreur. **Une extraction n'est jamais une qualification.**

## ULISTAG v0.1 — reconnaissance structurelle GED-01

`ulistag_v0.py` est le premier comparateur déterministe candidat fondé sur un graphe d'ancres textuelles et leurs relations géométriques.

Prérequis candidat : Python 3 et `pdfplumber>=0.11`.

Depuis la racine du dépôt :

```bash
python client/ulistag_v0.py match /chemin/vers/facture.pdf \
  --reference experiments/factures/GED-01/ulistag/reference_v0_1.json
```

Si le résultat est `MATCH_CANDIDATE`, l'extraction structurelle candidate peut être essayée :

```bash
python client/ulistag_v0.py extract /chemin/vers/facture.pdf \
  --profile experiments/factures/GED-01/profiles/sfr_structural_v0_1.json \
  --evidence-only
```

`--evidence-only` retourne les statuts de champs sans leurs valeurs. Le score de reconnaissance est une compatibilité structurelle déterministe, **pas une probabilité**. Aucun résultat v0.1 ne vaut qualification.

## TAG candidat

`tag_candidate.py` prépare localement un descripteur de TAG candidat à partir d'indices explicitement fournis. `test_tag_candidate.py` vérifie ce composant. Son protocole est documenté dans [project/TAG_CANDIDATE_PROTOCOL.md](../project/TAG_CANDIDATE_PROTOCOL.md).

## Reconnaissance de format

Le manque fonctionnel identifié relève de **HORIZON-FORMAT-001** : comparer une signature observée aux TAGs du catalogue, retourner une correspondance qualifiée, ambiguë ou inconnue, puis résoudre la liaison **TAG → profil d'extraction**.

## Positionnement

Le client n'appartient ni à GED-01, ni à GED-02, ni à une maturité particulière du catalogue. Une expérience peut fournir ses fixtures, profils, paramètres et critères de preuve ; le client reste générique et réutilisable.
