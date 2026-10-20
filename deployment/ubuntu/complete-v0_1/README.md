# ULISDOQ Complete Ubuntu v0.1

Point d'entrée canonique pour installer et vérifier **toutes les capacités logicielles actuellement déclarées** par ULISDOQ v0.1.

## Installer

Depuis un checkout Git propre et épinglé :

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh install \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1" \
  --install-system
```

L'option `--install-system` autorise explicitement l'installation APT. Sans elle, aucun paquet système n'est modifié.

## Vérifier

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh verify \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1"
```

La batterie produit une décision globale et une preuve par capacité.

## Rollback

```bash
bash deployment/ubuntu/complete-v0_1/ulisdoq-deploy.sh rollback \
  --root "$HOME/.local/share/ulisdoq/complete-v0_1"
```

Le rollback supprime uniquement les venvs appartenant au profil. Il conserve les preuves et ne désinstalle jamais automatiquement les paquets système.

## Environnements isolés

```text
core
anchor_graph
visual_keypoints
invoice2data
semantic_validation
```

Cette séparation évite qu'une contrainte de dépendances d'une capacité ne déstabilise les autres.

## GPU

Aucune capacité v0.1 ne requiert actuellement CUDA. Le GPU peut être observé mais n'est ni installé ni qualifié par ce profil.
