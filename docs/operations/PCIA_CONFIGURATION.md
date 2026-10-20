# PCIA — Configuration ULISDOQ qualifiée

**Cible : PCIA**  
**Identité exacte : PC-13333330**

Ce fichier ne contient que des états **vérifiés par preuve d'exécution**. Les exigences candidates ou les versions attendues sont conservées dans les manifestes de méthode, pas enregistrées ici comme installations acquises.

## État qualifié

Aucune nouvelle dépendance ULISDOQ / visual-keypoints n'est enregistrée comme installée ou vérifiée tant que le retour PCIA n'a pas été produit.

### Environnement historique à préserver

```text
pdfplumber local reader
version attendue d'après l'état antérieur : 0.11.10
statut dans ce document : À RE-VÉRIFIER LORS DU DÉPLOIEMENT
mutation autorisée : NON
```

## Entrée à ajouter après preuve

Pour chaque environnement déployé :

```text
METHOD_ID=
METHOD_VERSION=
SOURCE_COMMIT=

PYTHON_EXECUTABLE=
ENVIRONMENT_LOCATION=
DEPENDENCY_LOCK_SHA256=

INSTALLED_COMPONENTS=
  package=exact_version
  ...

SYSTEM_COMPONENTS=
  component=exact_version
  ...

VERIFICATION_RESULT=
PASS|FAIL

CAPABILITY_STATUS=
VERIFIED|NOT_VERIFIED

METHOD_QUALIFICATION=
NONE|PHASE1_CANDIDATE|PHASE1_QUALIFIED|...

PROFILE_QUALIFICATION=
<profile id + status>

EVIDENCE_REFERENCES=
...

INSTALLATION_DATE=
...
```

**Règle : ne jamais enregistrer une installation non vérifiée comme configuration qualifiée.**


## Rattachement au profil complet

Un environnement historique PCIA peut être réutilisé par `ULISDOQ-COMPLETE-UBUNTU-V0.1` uniquement par rattachement explicite :

```text
ENVIRONMENT_NAME=
PATH=
MODE=ATTACHED
LIVE_FREEZE_SHA256=
GLOBAL_VERIFICATION_RESULT=
```

Le rattachement :

- ne transfère pas la propriété de l'environnement à ULISDOQ ;
- interdit sa suppression par rollback ;
- ne signifie pas compatibilité tant que la batterie globale n'est pas PASS ;
- permet d'installer uniquement le delta manquant autour de l'existant.

Aucun rattachement n'est actuellement enregistré comme qualifié tant qu'un retour runtime PCIA n'a pas été reçu.
