# PCIA — Déploiement GED-02 / visual-keypoints v0.1

**Référence : PCIA-DEPLOY-GED02-VISUAL-KEYPOINTS-001**  
**Cible : PC-13333330**  
**Transport : GitHub + DEV-NAVETTE existant**  
**Nouveau transport : interdit**

## Objets canoniques

- méthode : `ULISTAG-VISUAL-KEYPOINTS-ORB-HAMMING-RANSAC`
- version : `0.1.0-phase1`
- source méthode : commit `1a999499779404a305cf2cf04c7ddb06627f48f1`
- dépendances : `requirements-pcia-v0_1.txt`
- SHA-256 lock : `c864f1a0fc66e9677cef18154f8347d29b9cba2c6730987c6795b3ccc15f9c0c`
- manifeste : `deployment_manifest_v0_1.json`
- vérification : `verify_capability_v0_1.py`

## Préflight

Avant toute mutation :

1. vérifier l'identité de PCIA ;
2. vérifier Python `3.12.3` et relever son chemin exact ;
3. vérifier le commit / worktree ULISDOQ utilisé ;
4. calculer le SHA-256 du fichier requirements et le comparer au manifeste ;
5. observer `tesseract --version` sans le modifier ;
6. observer l'environnement pdfplumber existant sans le modifier ;
7. choisir un chemin d'environnement virtuel **nouveau et dédié**.

Si une précondition diverge, arrêter avant installation.

## Installation autorisable

```bash
python3 -m venv <ULISDOQ_VENV>
<ULISDOQ_VENV>/bin/python -m pip install --upgrade pip
<ULISDOQ_VENV>/bin/python -m pip install   -r ULISTAG/matchers/visual_keypoints/requirements-pcia-v0_1.txt
```

Aucun `sudo pip`, aucun `pip --user`, aucune modification de l'environnement pdfplumber existant.

Tesseract est **vérifié seulement** dans cette passe. S'il est absent ou différent de `5.3.4`, retourner l'écart ; ne pas modifier le système sans autorisation distincte.

## Vérification

```bash
<ULISDOQ_VENV>/bin/python   ULISTAG/matchers/visual_keypoints/verify_capability_v0_1.py   > <EVIDENCE_DIR>/visual_keypoints_capability.json
```

Résultat requis :

```text
status=PASS
qualification=CAPABILITY_VERIFICATION_ONLY
```

Un PASS autorise l'usage expérimental de la méthode ; il ne qualifie ni la méthode au sens documentaire ni le profil GED-02.

## Rollback

En cas d'échec ou de retrait :

```text
stopper l'utilisation de l'environnement
conserver la preuve d'échec
supprimer uniquement <ULISDOQ_VENV>
supprimer éventuellement la copie de travail dédiée
ne pas toucher à pdfplumber
ne pas modifier Tesseract
```

## Retour attendu

Le retour PCIA fournit les champs requis par `docs/operations/PCIA_CONFIGURATION.md`. CLAU/LIFECYCLE décide ensuite de l'inscription dans la configuration qualifiée.
