# Organisation du dépôt ULISDOQ

**Version de structure : 2 — 29 octobre 2026**

Ce document décrit l'organisation simple du dépôt. Git constitue l'historique et le mécanisme de versionnement.

## Principe général

ULISDOQ construit d'abord un patrimoine de connaissance sur la **paperasserie française**.

L'arborescence métier est donc francophone autant que possible. L'anglais reste accepté dans les composants logiciels, les API, les schémas techniques, les standards et les concepts de développement lorsqu'il constitue l'usage naturel de la communauté.

## Branche de référence

`main` est la branche de travail normale et la référence courante du dépôt.

**Toute création d’une nouvelle branche exige une décision ou une confirmation explicite de Jean, avant sa création.** Aucun agent ou outil ne doit en créer de sa propre initiative, même pour un changement logiciel risqué, une refonte ou une expérimentation. Un tel besoin peut être proposé à Jean, avec son motif et sa durée prévue.

Le projet est actuellement en évaluation : le statut testing ne justifie pas à lui seul une séparation de branches. Le code, les tests, les profils candidats et la documentation retenus sont conservés dans `main`, avec leurs limites explicites.

## Surfaces principales

| Espace | Responsabilité |
| --- | --- |
| `catalogue/` | Connaissance documentaire réutilisable ; index et registre de profils avec statuts explicites. |
| `logiciels/` | ULISTAG, client, Profile Builder, escalade consommateur, déploiement et vérification. |
| `experiences/` | Cas GED, corpus autorisés, candidats expérimentaux et preuves. |
| `documentation/` | Architecture, méthode, état, décisions et études générales. |

Le code, les contrats, tests et documents propres restent auprès de chaque composant. Les preuves d'un cas restent dans son expérience. Les fichiers racine utiles sont README.md, PROLOGUE_FONDATEUR.md, AGENTS.md, CONTRIBUTING.md, VERSION et .gitignore.

Le registre `catalogue/registre-profils.json` peut référencer des candidats des expériences ; leur référencement ne les promeut pas au catalogue canonique. Les registres du Builder décrivent ses capacités logicielles et gardent leur rôle distinct.

La [correspondance de migration](../migration/CORRESPONDANCE_LOT_1.json) conserve les anciens chemins et les empreintes de départ. Ce document reste séparé jusqu'à l'examen de sa fusion avec l'architecture générale.


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

## Cycle de travail et versions

Pour le contributeur unique, le travail se fait dans `main`, avec des commits ciblés et vérifiés. Si Jean autorise expressément une branche temporaire, elle a un objectif précis et rejoint `main` ou est abandonnée après conservation des résultats utiles. Après rapatriement et vérification, sa référence secondaire est supprimée selon la décision de Jean ; les commits utiles restent conservés. Une branche ne sert pas d’archive permanente.

Les commits conservent l’historique ; les tags marquent les jalons reproductibles. Les versions des logiciels et profils restent indépendantes de celle du dépôt. Le point d’entrée courant est [documentation/ETAT_DU_PROJET.md](../ETAT_DU_PROJET.md).
