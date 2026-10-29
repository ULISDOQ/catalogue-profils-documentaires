# ULISDOQ — Matrice de compatibilité Ubuntu v0.1

**Profil : `ULISDOQ-COMPLETE-UBUNTU-V0.1`**

La compatibilité n'est **jamais déduite** du fait qu'une version est plus récente.

| Cible | Python | État |
|---|---|---|
| PCIA / Ubuntu 22.04.5 WSL2 x86_64 | 3.12.3 | **REFERENCE_PARTIAL** : plusieurs capacités ont été observées/testées séparément ; le profil complet reste à exécuter et confirmer par LIFECYCLE |
| Ubuntu 22.04.x x86_64 | 3.12.3 | **DEPLOYABLE_CANDIDATE** : doit passer la batterie globale |
| Ubuntu 24.04.x x86_64 | 3.12.x ou plus récent | **UNQUALIFIED_CANDIDATE** jusqu'à batterie globale réussie |
| autre Ubuntu / autre Python | quelconque | **UNQUALIFIED** jusqu'à preuve |

## Règle

Une cible devient une combinaison testée seulement après enregistrement de :

```text
OS exact
kernel
architecture
Python exact
paquets système résolus
locks Python exacts
résultats de vérification par capacité
commit ULISDOQ
```

Un Python supérieur à 3.12.3 est accepté pour **tentative de déploiement**, mais ne reçoit aucun statut de compatibilité avant la batterie globale.

## GPU / CUDA

Aucune capacité déclarée de `ULISDOQ-COMPLETE-UBUNTU-V0.1` n'exige actuellement CUDA.

Par conséquent :

```text
CUDA_DEPENDENCY=NO
GPU_FRAMEWORK_DEPENDENCY=NO
GPU_MODEL_DEPENDENCY=NO
```

Le déploiement peut relever `nvidia-smi` s'il existe, mais ne doit ni installer ni modifier pilote, CUDA, PyTorch GPU ou modèle. Une future capacité GPU provoquera une évolution versionnée du profil et de cette matrice.
