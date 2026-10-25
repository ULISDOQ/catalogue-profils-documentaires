# Organisation du dépôt ULISDOQ

**Version de structure : 1.0 — 25 octobre 2026**

Ce document décrit l'organisation simple du dépôt. Git constitue l'historique et le mécanisme de versionnement.

## Principe général

ULISDOQ construit d'abord un patrimoine de connaissance sur la **paperasserie française**.

L'arborescence métier est donc francophone autant que possible. L'anglais reste accepté dans les composants logiciels, les API, les schémas techniques, les standards et les concepts de développement lorsqu'il constitue l'usage naturel de la communauté.

## Branche de référence

`main` est la branche de travail normale et la référence courante du dépôt.

Une branche séparée n'est utilisée que lorsqu'un développement logiciel risqué, une refonte importante ou une expérimentation pouvant casser l'existant le justifie.

## Surfaces principales

```text
catalogue/
    connaissance documentaire canonique et réutilisable

experiences/
    cas GED, preuves, corpus autorisés, essais et RETEX

escalade-consommateur/
    contrat générique de demande documentaire et de retour vers un consommateur

profile-builder/
    sous-projet logiciel ; terminologie de développement anglaise conservée

ULISTAG/
    capacités de reconnaissance documentaire

client/
    adaptateurs et outils exécutables

project/
    architecture et documents de conception transverses
```

## Catalogue

Le catalogue est classé par catégorie documentaire :

```text
catalogue/
  index.json
  profils/
    <domaine>/
      <juridiction>/
        <categorie-documentaire>/
          <identifiant-profil>/
            <version>/
```

Un profil n'est pas classé selon l'employeur, le logiciel producteur ou le numéro GED.

## Expériences

Une expérience est un cas d'étude versionné :

```text
experiences/
  factures/
  impots-finances/
  administration-droits/
  assurances/
  paye/
  ...
```

Le numéro GED appartient à l'expérience, pas à l'identité canonique du profil.

## Règle de simplicité

Lorsqu'une connaissance est réutilisable, elle monte dans le catalogue.

Lorsqu'un élément sert uniquement à démontrer, tester ou documenter un cas, il reste dans `experiences/`.

Lorsqu'un élément est du logiciel générique, il reste dans le composant logiciel concerné.

Cette séparation doit éviter que les essais du Profile Builder ou d'un autre outil dictent l'organisation documentaire d'ULISDOQ.
