# ULISDOQ — Notice des dépendances logicielles

**Référence : ULISDOQ-SOFTWARE-DEPENDENCY-NOTICE-001**

PCIA est enrichie progressivement pendant les expériences GED-N. **L'état logiciel de PCIA n'est pas, à lui seul, le contrat de déploiement d'un consommateur.**

La chaîne de capitalisation est :

```text
GED-N
→ besoin logiciel observé
→ installation autorisée sur PCIA
→ capacité vérifiée
→ RETEX
→ dépendance classée
→ inventaire ULISDOQ versionné
→ réemploi sur d'autres consommateurs
```

## Classification

Une dépendance appartient à l'une des catégories suivantes :

- **BASE** : nécessaire au déploiement général ULISDOQ ;
- **CAPABILITY** : nécessaire à une capacité déclarée particulière ;
- **EXPERIMENTAL** : rencontrée mais pas encore retenue dans le profil complet ;
- **RETIRED** : conservée pour reconstructibilité mais non déployée.

L'inventaire canonique de la version actuelle est :

`logiciels/deploiement/ubuntu/complete-v0_1/capability_inventory.json`

## Règle d'évolution

Le profil `ULISDOQ-COMPLETE-UBUNTU-V0.1` contient **toutes les capacités déclarées de cette version**, et seulement celles-ci.

Lorsqu'une expérience introduit une nouvelle capacité durable :

1. créer ou compléter son manifeste ;
2. qualifier sa dépendance comme CAPABILITY ;
3. ajouter son test fonctionnel ;
4. faire évoluer le profil complet de manière versionnée ;
5. ne jamais considérer une installation opportuniste sur PCIA comme un prérequis universel implicite.

## Reconstruction d'un consommateur

Un consommateur doit pouvoir être installé sans connaître l'histoire de PCIA à partir de :

```text
profile_manifest.json
capability_inventory.json
apt-packages.txt
requirements-*.txt
ulisdoq-deploy.sh
verify_complete.py
COMPATIBILITY.md
```

Les locks exacts produits sur une cible qualifiée sont des preuves et deviennent des références de reproduction après décision explicite.

## États

```text
INSTALLED
!=
CAPABILITY_VERIFIED
!=
METHOD_QUALIFIED
!=
PROFILE_QUALIFIED
!=
PRODUCTION_QUALIFIED
```
