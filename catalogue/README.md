# Catalogue ULISDOQ

Ce répertoire constitue la surface canonique de connaissance documentaire réutilisable.

Il est distinct de :
- `experiences/` : cas réels, preuves, essais et dettes de recherche ;
- `profile-builder/` : sous-projet logiciel de construction et de planification de profils ;
- `ULISTAG/` : capacités de reconnaissance documentaire ;
- `client/` : adaptateurs et outils exécutables.

## Principe de classement

Le catalogue est organisé selon la **catégorie documentaire**, et non selon le numéro d'expérience, l'employeur, l'éditeur logiciel ou l'implémentation courante.

```text
catalogue/
  index.json
  profils/
    <domaine>/
      <juridiction>/
        <categorie-documentaire>/
          <identifiant-profil>/
            <version>/
              profile.json
              grammar.json
              QUALIFICATION.md
              EVIDENCE.md
```

Les noms de fichiers et objets techniques peuvent rester en anglais lorsque cette terminologie est celle de l'ingénierie ou d'un contrat logiciel stabilisé.

## Identité d'une catégorie

Un profil de catégorie contient l'énoncé minimal qui définit l'identité documentaire.

Tout le reste relève de :
- la grammaire sémantique ;
- la grammaire d'extraction ;
- la variation observée ;
- d'éventuels adaptateurs spécialisés ;
- la preuve de qualification.

Pour GED-05 :

```text
CATEGORIE = BULLETIN_DE_PAIE_FRANCAIS
INVARIANT_DE_CATEGORIE = DOCUMENT_IS_A_FRENCH_PAYSLIP
```

L'identité de l'employeur ou du salarié, le logiciel de paie, la mise en page exacte, les coordonnées, libellés et codes de paie ne sont pas des invariants de catégorie.

## Frontière de promotion

Un profil `CANDIDATE_UNQUALIFIED` peut exister dans le catalogue afin d'être étudié et éprouvé.

Sa présence dans `catalogue/` ne le rend pas automatiquement sélectionnable.

Construction, qualification et publication restent distinctes.
