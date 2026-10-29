# ULISDOQ — Contrat réutilisable de déploiement de méthode

**Référence : ULISDOQ-DEPLOYMENT-CONTRACT-001**  
**Statut : CANDIDAT OPÉRATIONNEL — PHASE 1**

Déployer ULISDOQ sur une cible signifie déployer **le code, la méthode, ses dépendances déclarées, ses tests de capacité et les preuves d'exécution**. La simple présence d'un paquet n'est jamais assimilée à une capacité qualifiée.

## Contrat obligatoire par méthode

Chaque méthode déployable doit déclarer :

```text
METHOD_ID
METHOD_VERSION
SOURCE_COMMIT
IMPLEMENTATION_PATH

REQUIRED_CAPABILITIES

PYTHON_DEPENDENCIES
SYSTEM_DEPENDENCIES
VERSION_CONSTRAINTS

ISOLATED_ENVIRONMENT
INSTALLATION_PROCEDURE
VERIFICATION_PROCEDURE
ROLLBACK_PROCEDURE

EXPECTED_EVIDENCE
QUALIFICATION_SEMANTICS
```

Le manifeste canonique est placé **au plus près de la méthode** :

`logiciels/ULISTAG/matchers/<method>/deployment_manifest_<version>.json`

Les dépendances Python exactes sont conservées dans le même répertoire sous forme d'un fichier `requirements-*.txt` dont le SHA-256 est inscrit dans le manifeste.

## États à ne pas confondre

```text
DEPENDENCY_INSTALLED
!=
CAPABILITY_VERIFIED
!=
METHOD_QUALIFIED
!=
PROFILE_QUALIFIED
!=
PRODUCTION_QUALIFIED
```

- **DEPENDENCY_INSTALLED** : paquet ou outil présent.
- **CAPABILITY_VERIFIED** : le test de capacité canonique passe sur la cible.
- **METHOD_QUALIFIED** : les expériences prévues pour la méthode ont produit les preuves requises.
- **PROFILE_QUALIFIED** : un profil documentaire particulier satisfait son protocole de qualification.
- **PRODUCTION_QUALIFIED** : décision ultérieure distincte ; jamais implicite en phase 1.

## Installation

Les dépendances Python sont installées dans un environnement virtuel isolé. Aucun `pip` global n'est autorisé.

Procédure générique :

```bash
python3 -m venv <ENV_PATH>
<ENV_PATH>/bin/python -m pip install --upgrade pip
<ENV_PATH>/bin/python -m pip install -r <REQUIREMENTS_FILE>
<ENV_PATH>/bin/python <VERIFY_SCRIPT>
```

Sous Windows natif, utiliser les exécutables équivalents de `Scripts\python.exe`.

L'identité du dépôt et des fichiers de méthode doit être contrôlée avant installation/exécution. En cas de dérive non résolue : **FAIL CLOSED**.

## Dépendances système

Une dépendance système existante est d'abord **observée et vérifiée**. Son installation ou sa modification nécessite une autorisation distincte lorsqu'elle sort du périmètre déjà approuvé.

## Rollback

Le rollback d'une méthode Python isolée consiste à supprimer :

1. l'environnement virtuel dédié ;
2. la copie de travail déployée si elle a été créée uniquement pour ce déploiement.

Le rollback ne modifie pas l'environnement Python existant, les lecteurs déjà qualifiés ni les dépendances système sans ordre explicite.

## Evidence minimale

Le retour cible doit contenir :

```text
TARGET_ID
SOURCE_COMMIT
METHOD_ID
METHOD_VERSION
PYTHON_EXECUTABLE
ENVIRONMENT_PATH
REQUIREMENTS_SHA256

INSTALLED_COMPONENTS_AND_VERSIONS
CAPABILITY_TEST_RESULT
CAPABILITY_TEST_OUTPUT_REF

INSTALLATION_DATE
QUALIFICATION_STATUS
EVIDENCE_REFERENCES
```

Aucune donnée documentaire privée n'est requise dans la preuve de déploiement.
