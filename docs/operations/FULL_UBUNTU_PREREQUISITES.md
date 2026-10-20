# ULISDOQ FULL — Prérequis Ubuntu réutilisables

**Référence : ULISDOQ-FULL-UBUNTU-PREREQUISITES-001**  
**Statut : CANDIDAT PHASE 1**

## Finalité

Ce profil n'est pas dérivé d'un seul cas documentaire. Il constitue la pile logicielle générale de laboratoire ULISDOQ destinée à supporter la majorité des besoins prévisibles de GED-01 à GED-70 sans réinstaller un environnement à chaque expérience.

Il couvre PDF texte et image, rendu PDF, OCR, traitement d'image, reconnaissance ULISTAG, tableaux, formats bureautiques courants, codes-barres/QR, validation structurée, synchronisation du catalogue, tests, preuves, ainsi qu'une base ML/GPU candidate.

## Baseline cible

~~~text
OS          Ubuntu >= 22.04 LTS
ARCH        x86_64
PYTHON      >= 3.12.3
GPU         NVIDIA CUDA-capable
GPU CLASS   >= RTX 4060 8 GB pour le profil GPU complet
CUDA        >= baseline effectivement observée sur PCIA
~~~

La version exacte du driver NVIDIA et la capacité CUDA de PCIA ne sont pas encore présentes dans la configuration qualifiée. Elles doivent être observées avant de déclarer qu'une autre cible est réellement supérieure ou égale à PCIA.

La règle est donc : ne pas inventer le baseline CUDA.

## Portée FULL

FULL signifie : installer à l'avance les capacités logicielles déjà identifiées comme utiles au périmètre ULISDOQ phase 1, même si GED-N ne les utilise pas toutes.

FULL ne signifie pas : installer toute dépendance imaginable d'un futur ULISDOQ encore inconnu. Une nouvelle capacité est ajoutée au manifeste FULL lorsqu'elle devient une capacité retenue par le projet.

## Familles de capacités

~~~text
base runtime
PDF IO / rendering
document parsing
image processing
OCR
layout / matching
tables / structured data
office formats
barcode / QR
semantic validation
HTTP / catalogue sync
testing / evidence
GPU / ML
~~~

## Installation complète

Depuis un checkout Git épinglé :

~~~bash
cd catalogue-profils-documentaires

python3 deployment/linux/verify_host_v0_1.py

ULISDOQ_INSTALL_SYSTEM_PACKAGES=YES   bash deployment/ubuntu/full/install_full_v0_1.sh   /opt/ulisdoq/venvs/full-v0_1   /opt/ulisdoq/evidence/full-v0_1
~~~

Le script refuse de modifier un venv existant. Les paquets système ne sont installés que lorsque la variable d'autorisation explicite vaut YES.

Après installation, le jeu exact réellement résolu par pip est gelé dans :

~~~text
requirements-full-resolved.txt
requirements-full-resolved.sha256
~~~

Ce premier lock exact doit être capitalisé comme lock canonique seulement après qualification réussie sur PCIA.

## Pile système

Le fichier deployment/ubuntu/full/apt-packages-v0_1.txt prévoit notamment :

- Git, CA, curl, jq ;
- compilation Python native ;
- Poppler ;
- qpdf ;
- Ghostscript ;
- Tesseract FR/EN ;
- bibliothèques OpenCV ;
- zbar ;
- bibliothèques XML et image.

## Pile Python

Le fichier deployment/ubuntu/full/requirements-full-v0_1.in couvre :

- contrats et validation JSON/YAML ;
- PDF ;
- image / vision ;
- OCR ;
- matching ;
- tableaux ;
- formats DOCX/ODS/XLSX ;
- codes-barres ;
- invoice2data ;
- tests ;
- PyTorch / Transformers / ONNX Runtime GPU.

Les dépendances déjà éprouvées pour GED-02 restent exactement contraintes ; les nouvelles capacités FULL restent à contrainte minimale jusqu'au premier déploiement complet réussi sur PCIA, qui produira le lock exact de référence.

## NVIDIA / CUDA

Le protocole n'installe ni ne remplace automatiquement le driver NVIDIA ni CUDA.

Ces composants dépendent du matériel, du noyau et du mode natif/WSL. Le test FULL relève :

~~~text
GPU
VRAM
NVIDIA driver
CUDA capability reported by nvidia-smi
PyTorch CUDA runtime
torch.cuda.is_available()
compute capability
~~~

Pour comparer une nouvelle cible à PCIA, ces observations sont confrontées au baseline PCIA enregistré dans docs/operations/PCIA_CONFIGURATION.md.

Si ce baseline manque :

~~~text
GPU_COMPARISON=UNRESOLVED
~~~

et jamais PASS par hypothèse.

## Deux niveaux de vérification

CPU_DOCUMENT_STACK_PASS signifie que le socle documentaire complet fonctionne sans GPU.

GPU_STACK_PASS signifie en plus que la chaîne NVIDIA/CUDA/PyTorch est opérationnelle.

Une expérience n'utilisant pas le GPU peut avancer avec le premier niveau.

## Réemploi

Une fois la pile FULL qualifiée sur une machine :

~~~text
GED-N
→ vérifier l'intégrité du bundle FULL
→ réutiliser les capacités existantes
→ ajouter seulement un delta si une capacité réellement nouvelle apparaît
~~~

C'est ce profil FULL, et non le manifeste d'un seul matcher, qui doit devenir le prérequis standard d'une machine de laboratoire ULISDOQ.

## Limites et dettes

- PyMuPDF reste à examiner juridiquement avant industrialisation de production.
- Tesseract ne garantit pas une lecture manuscrite avancée ; le bundle GPU permet d'expérimenter d'autres lecteurs.
- Le premier déploiement FULL réussi sur PCIA doit produire le lock exact canonique.
- Le baseline CUDA/driver de PCIA doit être observé et capitalisé avant comparaison stricte avec une autre cible.
