# ULISDOQ Complete Ubuntu v0.1

Point d'entrée canonique pour installer et vérifier **toutes les capacités logicielles actuellement déclarées** par ULISDOQ v0.1.

## Principe : rattacher puis installer le delta

Sur une machine déjà utilisée, notamment PCIA, le profil complet **ne doit pas reconstruire automatiquement ce qui existe déjà**.

Un environnement existant peut être rattaché explicitement :

```bash
--attach anchor_graph=/chemin/vers/venv-existant
```

Le rattachement n'est accepté comme compatible qu'après passage de la batterie globale. Un environnement non possédé par ce profil et non explicitement rattaché provoque un arrêt fail-closed.

Les environnements absents sont créés ; les environnements possédés déjà présents sont réutilisés ; les paquets APT déjà installés ne sont pas réinstallés.

## Installer

Sur une machine neuve :

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh install \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1" \
  --install-system
```

Sur PCIA ou une machine déjà équipée, exemple de rattachement :

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh install \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1" \
  --attach anchor_graph=/chemin/venv-pdfplumber \
  --attach visual_keypoints=/chemin/venv-visual
```

Ne pas ajouter `--install-system` si aucun paquet système manque ou si l'installation système n'a pas été explicitement autorisée.

## Vérifier

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh verify \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1"
```

La batterie vérifie notamment :

- TAG candidat du client ;
- versions et fonctions de `anchor_graph` ;
- ORB / Hamming / RANSAC / rendu PDF de `visual_keypoints` ;
- Tesseract + données linguistiques FR/EN ;
- **OCR fonctionnel sur une image synthétique** ;
- chargement et **extraction fonctionnelle minimale invoice2data** ;
- validation du schéma sémantique ;
- Poppler ;
- identité Git ;
- locks ou freeze live des environnements rattachés.

## Rollback protégé

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh rollback \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1"
```

Le rollback nécessite :

- le marqueur de propriété du profil ;
- l'état `environments.tsv` ;
- un marqueur propre dans chaque venv possédé ;
- un chemin restant sous la racine du profil.

Il supprime **uniquement** les venvs créés et marqués comme possédés par ce profil. Les environnements rattachés, preuves et paquets système sont conservés.

## Environnements isolés

```text
core
anchor_graph
visual_keypoints
invoice2data
semantic_validation
```

## Limites actuelles de reproductibilité

- le profil complet n'a pas encore été exécuté et qualifié sur PCIA ;
- un environnement PCIA rattaché est une combinaison observée, pas automatiquement un lock canonique ;
- son `pip freeze` est hashé comme preuve pendant la vérification ;
- les versions exactes des paquets APT résolus dépendent de l'état des dépôts Ubuntu au moment de l'installation et doivent être enregistrées lors de la qualification ;
- Ubuntu ou Python plus récents ne sont jamais supposés compatibles sans batterie globale réussie ;
- aucune capacité v0.1 ne requiert CUDA/GPU.

## GPU

CUDA et les frameworks GPU ne font pas partie du profil v0.1. Une future capacité GPU entraînera une évolution versionnée du profil.
