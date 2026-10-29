# Vérifier le dépôt depuis une copie propre

Ces contrôles vérifient les ressources et contrats publiés, les vecteurs synthétiques et les limites déclarées. Ils ne déploient aucun consommateur et n’utilisent aucun document personnel source.

Prérequis : Python 3.12 ou version compatible à éprouver, Git pour récupérer le dépôt. Les dépendances de test sont déclarées dans [dépendances de vérification](requirements.txt).

```bash
git clone https://github.com/ULISDOQ/catalogue-profils-documentaires.git
cd catalogue-profils-documentaires
git rev-parse HEAD
python3 -m venv .venv
.venv/bin/python -m pip install -r logiciels/verification/requirements.txt
.venv/bin/python logiciels/verification/verifier_depot.py
```

Ces commandes vérifient main et affichent son commit exact. Pour reconstruire une observation antérieure, exécuter `git checkout COMMIT_OBSERVE` avant les tests, en remplaçant COMMIT_OBSERVE par l’empreinte conservée dans le compte rendu. Le tag d’évaluation reste prévu mais non créé. Après installation de la dépendance, le vérificateur n’a pas besoin du réseau.

Le contrôle couvre les chemins actifs, liens Markdown, registres, empreintes, référence visuelle GED-02, neuf courriels synthétiques GED-03, catalogue GED-05, cycle GED-04 et sélection des matchers du Builder. Il vérifie aussi les octets du manifeste de distribution courant.

GED-02 conserve son écart connu de ligne 420 et les profils restent candidats. Les suites n’exécutent pas les moteurs OpenCV, OCR ou invoice2data ; leur qualification et le déploiement complet Ubuntu relèvent de leurs procédures propres.

Résultats historiques du rangement : [contrôle du 25 octobre](../../documentation/preuves/COHERENCE_VERTICALES_2026-10-25.md). Résultats de consolidation : [compte rendu](../../documentation/preuves/CONSOLIDATION_2026-10-25.md).
