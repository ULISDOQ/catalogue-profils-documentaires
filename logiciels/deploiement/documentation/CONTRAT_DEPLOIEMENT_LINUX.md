# ULISDOQ — Contrat de déploiement Linux

**Référence : ULISDOQ-LINUX-DEPLOYMENT-CONTRACT-001**  
**Statut : CANDIDAT OPÉRATIONNEL — PHASE 1**

## 1 — Objet

Ce contrat décrit les prérequis et l'ordre de déploiement nécessaires pour installer sur un hôte Linux donné :

1. le dépôt / client ULISDOQ ;
2. le cœur ULISTAG ;
3. les méthodes ULISTAG effectivement demandées ;
4. les lecteurs / moteurs d'extraction optionnels nécessaires au cas d'usage ;
5. les tests de capacité et les preuves de déploiement.

Deux modes existent :

- **profil complet** : installe toutes les capacités déclarées par une version ULISDOQ ; c'est le mode canonique pour une nouvelle machine de laboratoire ou un consommateur complet ;
- **bundle de capacité** : installe seulement une capacité explicitement choisie ; utile pour une cible contrainte.

Le profil complet canonique courant est `ULISDOQ-COMPLETE-UBUNTU-V0.1` sous `logiciels/deploiement/ubuntu/complete-v0_1/`.

Le déploiement par capacité reste un mécanisme de composition interne et ne remplace pas le contrat complet lorsqu'un déploiement ULISDOQ complet est demandé.

```text
BESOIN
→ CAPACITÉS REQUISES
→ MÉTHODES ULISDOQ/ULISTAG
→ DÉPENDANCES EXACTES
→ INSTALLATION ISOLÉE
→ TESTS DE CAPACITÉ
→ PREUVE
```

## 2 — Couches de déploiement

### L0 — Hôte Linux

Prérequis minimaux :

- Linux 64 bits ;
- shell POSIX / bash ;
- Git ;
- accès HTTPS sortant vers GitHub si synchronisation distante requise ;
- certificats CA système fonctionnels ;
- Python 3.12.x ;
- module `venv` disponible ;
- `pip` utilisable **dans un environnement virtuel seulement** ;
- utilitaire de calcul SHA-256.

Architecture actuellement éprouvée : `x86_64`.

Toute autre architecture est possible en théorie mais reste `UNQUALIFIED` tant qu'un test de capacité n'a pas été exécuté.

### L1 — Source ULISDOQ

Le code est obtenu depuis GitHub puis épinglé sur un commit explicite.

Exemple :

```bash
git clone https://github.com/ULISDOQ/catalogue-profils-documentaires.git
cd catalogue-profils-documentaires
git checkout <PINNED_COMMIT>
git status --short
git rev-parse HEAD
```

Conditions :

- le HEAD doit être exactement celui attendu ;
- le worktree doit être propre avant qualification ;
- aucune exécution n'est autorisée en cas de dérive de source non résolue.

### L2 — Client ULISDOQ

Le répertoire `logiciels/client/` constitue le client transverse.

Les dépendances sont déterminées par la fonction utilisée :

| Fonction | Dépendances |
|---|---|
| TAG candidat | Python standard library |
| Extraction invoice2data | paquet Python `invoice2data` + lecteur compatible |
| Reconnaissance ULISTAG | dépend du matcher sélectionné |
| OCR | dépend du lecteur OCR sélectionné |

Dans le **profil complet**, toutes les capacités déclarées de la version sont orchestrées et installées dans des environnements isolés distincts. Dans un bundle minimal, seules les dépendances demandées sont installées.

### L3 — ULISTAG cœur

Le répertoire `logiciels/ULISTAG/` est déployé avec le dépôt.

Chaque matcher possède son propre manifeste de dépendances sous :

`logiciels/ULISTAG/matchers/<matcher>/deployment_manifest_<version>.json`

Le déploiement sélectionne uniquement les matchers nécessaires.

Exemples actuels :

- `anchor_graph` : lecteur PDF avec texte + coordonnées ;
- `visual_keypoints` : rendu PDF + ORB + Hamming + RANSAC.

### L4 — Lecteurs et moteurs optionnels

Les outils système ne sont installés que si le cas l'exige.

Exemples :

- Tesseract pour OCR ;
- autres lecteurs / OCR à venir.

Leur présence n'est jamais assimilée à une qualification de méthode.

## 3 — Arbre de décision de dépendances

```text
ULISDOQ CLIENT
│
├── TAG candidat seulement
│   └── Python standard library
│
├── extraction invoice2data
│   ├── venv dédié
│   ├── invoice2data
│   └── lecteur/OCR compatible
│
├── ULISTAG anchor_graph
│   ├── venv dédié
│   └── pdfplumber version déclarée
│
└── ULISTAG visual_keypoints
    ├── venv dédié
    ├── opencv-python-headless
    ├── numpy
    └── PyMuPDF
```

Une même cible peut partager un environnement seulement si le manifeste l'autorise explicitement et si les versions sont compatibles.

Par défaut :

> **un environnement virtuel par bundle de capacités qualifié.**

## 4 — Convention d'installation

Chemins indicatifs :

```text
/opt/ulisdoq/
├── source/<commit>/
├── venvs/<bundle-id>/
├── cache/
├── evidence/
└── runtime/
```

ou équivalent dans le HOME d'un utilisateur non privilégié.

Aucun chemin n'est normatif ; ce qui est obligatoire est :

- isolation ;
- identité exacte ;
- reconstructibilité ;
- possibilité de rollback ;
- absence de collision avec des environnements existants.

## 5 — Préflight obligatoire

Avant installation :

```bash
uname -a
uname -m
git --version
python3 --version
python3 -m venv --help >/dev/null
python3 -m pip --version
sha256sum --version
```

Puis relever :

```text
HOSTNAME
OS_ID
OS_VERSION
KERNEL
ARCH
GIT_VERSION
PYTHON_EXECUTABLE
PYTHON_VERSION
PIP_VERSION
NETWORK_TO_GITHUB
SOURCE_COMMIT
WORKTREE_CLEAN
```

Si un prérequis manque :

`PRECHECK=FAIL`

et aucune installation Python n'est entreprise avant décision.

## 6 — Installation Python

Règle :

```text
NO_GLOBAL_PIP
NO_PIP_USER
NO_MUTATION_OF_EXISTING_VENV
```

Procédure :

```bash
python3 -m venv <VENV>
<VENV>/bin/python -m pip install --upgrade pip
<VENV>/bin/python -m pip install -r <PINNED_REQUIREMENTS>
```

Le fichier requirements doit :

- être versionné ;
- contenir des versions exactes ;
- avoir un SHA-256 attendu dans le manifeste de méthode.

## 7 — Dépendances système

Les dépendances système sont gérées séparément des paquets Python.

Pour chaque outil système :

```text
NAME
PURPOSE
REQUIRED_VERSION_OR_RANGE
OBSERVED_VERSION
INSTALLATION_REQUIRED
INSTALLATION_AUTHORIZED
VERIFICATION_RESULT
```

L'installation via `apt`, `dnf`, `pacman` ou autre gestionnaire n'est **jamais implicite**.

Le contrat de méthode indique la capacité attendue ; le déploiement Linux adapte la procédure au gestionnaire de paquets de l'hôte après autorisation.

## 8 — Vérification

Après installation, exécuter :

1. test de présence ;
2. test de version ;
3. test fonctionnel minimal de chaque capacité ;
4. test de la méthode concernée ;
5. éventuellement test du profil documentaire.

Exemple de chaîne :

```text
dependency present
→ exact version
→ primitive works
→ matcher works
→ profile test works
```

Chaque étape a son statut propre.

## 9 — Qualification

```text
HOST_PRECHECK_PASS
!=
DEPENDENCIES_INSTALLED
!=
CAPABILITY_VERIFIED
!=
METHOD_QUALIFIED
!=
PROFILE_QUALIFIED
!=
PRODUCTION_QUALIFIED
```

La phase 1 s'arrête normalement à :

```text
HOST_PRECHECK_PASS
+
CAPABILITY_VERIFIED
+
PHASE1_METHOD_EVIDENCE
+
PHASE1_PROFILE_EVIDENCE
```

## 10 — Rollback

Rollback standard :

- supprimer le venv dédié ;
- supprimer la copie de source dédiée si elle n'est plus utile ;
- conserver les preuves ;
- ne pas toucher aux environnements historiques ;
- ne pas désinstaller un outil système partagé sans autorisation explicite.

## 11 — Evidence minimale de déploiement

```json
{
  "target": {
    "hostname": "...",
    "os_id": "...",
    "os_version": "...",
    "kernel": "...",
    "arch": "..."
  },
  "source": {
    "repository": "ULISDOQ/catalogue-profils-documentaires",
    "commit": "...",
    "worktree_clean": true
  },
  "python": {
    "executable": "...",
    "version": "...",
    "venv": "..."
  },
  "bundle": {
    "id": "...",
    "requirements_sha256": "...",
    "installed": {}
  },
  "system_tools": {},
  "verification": {
    "status": "PASS|FAIL",
    "evidence_refs": []
  },
  "qualification": {
    "capability": "VERIFIED|NOT_VERIFIED",
    "method": "...",
    "profile": "..."
  }
}
```

## 12 — Principe de réemploi

Lorsqu'une nouvelle expérience GED-N commence :

1. déclarer les capacités nécessaires ;
2. rechercher un bundle déjà présent et qualifié ;
3. réutiliser ce bundle si compatible ;
4. installer seulement le delta manquant ;
5. ne créer une nouvelle combinaison de dépendances que si nécessaire.

Le déploiement devient ainsi progressivement moins coûteux avec l'accumulation des GED-N.


## 13 — Profil complet Ubuntu canonique

Référence :

`logiciels/deploiement/ubuntu/complete-v0_1/`

Point d'entrée unique :

```bash
bash logiciels/deploiement/ubuntu/complete-v0_1/ulisdoq-deploy.sh install --install-system
```

Vérification globale :

```bash
bash logiciels/deploiement/ubuntu/complete-v0_1/ulisdoq-deploy.sh verify
```

Le profil complet possède :

- un inventaire versionné des capacités ;
- des manifests par capacité/méthode ;
- des environnements Python isolés ;
- des prérequis système déclarés ;
- une matrice de compatibilité ;
- une batterie globale ;
- un rollback borné.

Une capacité nouvelle issue d'un GED-N doit faire évoluer cet inventaire de manière versionnée.
