# Client ULISDOQ — démonstrateur invoice2data

**Ce code est un adaptateur local candidat, non encore validé sur la facture SFR.** Il lit un fichier local, charge le profil YAML du catalogue et appelle l'API Python publique d'[invoice2data](https://invoice2data.readthedocs.io/stable/usage.html). Aucun serveur, compte, service distant ou accès CLAU n'est requis.

## Prérequis

Python 3, \`invoice2data\`, et un moteur OCR local pour le PDF scanné. Voir [les dépendances OCR](https://invoice2data.readthedocs.io/stable/installation.html) ; pour \`--reader tesseract\`, installer Tesseract et ImageMagick ainsi que les données de langue nécessaires.

Depuis la racine du dépôt :

\`\`\`bash
python -m pip install invoice2data
python experiments/GED-01/client/extract.py \
  experiments/GED-01/fixtures/SFR_EXP01_document_experimental.pdf \
  --reader tesseract > resultat.json
\`\`\`

Le résultat est un JSON sur la sortie standard avec \`status\`, \`source_sha256\`, \`engine\`, \`reader\` et \`data\` (si extraction). Codes retour : 0 extraction non vérifiée ; 1 aucun profil reconnu ; 2 erreur. **Une extraction n'est jamais une qualification**.

## Intégration dans un client tiers (CLAU, GED, script...)

Un client récupère une version précise du catalogue, conserve son identifiant de commit, choisit un profil YAML, exécute localement l'adaptateur sur son propre document, puis compare le JSON aux contrôles métier. **Aucune donnée de document n'est transmise à ULISDOQ.** Ce client peut ensuite archiver la preuve dans son propre SI.

La compatibilité et la qualité OCR du modèle SFR sont à vérifier : le profil YAML est un point de départ, pas un résultat validé. Ne pas automatiser une mise en production sur cette base.
