# GED-02 — Relier un formulaire administratif à la connaissance officielle publiée

**Statut : expérience conceptuelle candidate, non qualifiée.**

Cette expérience ne vise pas d'abord la fiscalité comme domaine métier. Son objet principal est d'éprouver une capacité fondatrice d'ULISDOQ : **partir d'un document administratif identifiable et le relier à la connaissance officielle publiée par l'administration française**.

Le formulaire 2044 sert ici de cas concret parce qu'il appartient à un corpus public structuré : formulaire, millésime, notice, références administratives, règles et documentation associée peuvent être recherchés, sourcés, versionnés et reliés.

## Question expérimentale

À partir d'un document local ou de ses caractéristiques non sensibles, ULISDOQ doit pouvoir rechercher et restituer les connaissances publiques pertinentes autour de ce document, par exemple :

- la source administrative officielle ;
- l'identité et la version du formulaire ;
- la notice ou documentation associée ;
- les millésimes et variantes connus ;
- les règles ou références publiques utiles à son interprétation ;
- les profils d'extraction candidats et leurs limites ;
- la provenance et la date des connaissances utilisées.

L'objectif n'est donc pas seulement :

```text
document → profil d'extraction
```

mais également :

```text
document identifiable
→ source officielle publiée
→ connaissances documentaires associées
→ version / provenance / limites
→ profils et capacités techniques réutilisables
```

## Cas 2044

Le profil candidat est [profiles/fr_formulaire_2044_candidate.json](profiles/fr_formulaire_2044_candidate.json).

Il retient une famille de déclaration de revenus fonciers, le numéro de formulaire déclaré et des indices à vérifier sur des sources officielles datées. Les versions annuelles, annexes et variantes doivent être distinguées.

La présence du numéro « 2044 » ou de termes fiscaux n'est pas suffisante à elle seule pour qualifier le document ou sa version. La connaissance retenue doit être reliée à des sources officielles et explicitement datées.

## Ce que doit démontrer GED-02

GED-02 doit montrer qu'ULISDOQ sait :

1. reconnaître ou caractériser suffisamment un document administratif ;
2. retrouver une ou plusieurs références officielles candidates ;
3. établir un lien sourcé entre document, version et connaissance publiée ;
4. conserver les distinctions entre document, source de connaissance, TAG, profil et moteur ;
5. signaler `UNKNOWN` ou `AMBIGUOUS` lorsque la version ou la correspondance n'est pas suffisamment établie ;
6. réutiliser cette connaissance sans dépendre d'un moteur d'extraction particulier.

## Frontière avec l'extraction

Le TAG peut être préparé localement avec l'[éditeur ULISDOQ](../../../client/tag_candidate.py), puis comparé à un catalogue versionné.

Mais **l'extraction n'est pas le cœur de cette expérience**. Un moteur compatible pourra être choisi ensuite, lorsque l'identité documentaire, sa version et les sources officielles pertinentes auront été suffisamment établies.

Aucun document fiscal personnel réel n'est requis dans le dépôt pour conduire cette expérimentation.

## Critère de preuve

La preuve attendue est une chaîne reconstructible :

```text
document / caractéristiques observées
→ identification candidate du formulaire
→ source officielle
→ version ou millésime
→ connaissance publiée associée
→ provenance vérifiable
→ éventuel profil d'extraction candidat
```

Une simple reconnaissance textuelle ou la présence d'un profil dans le dépôt ne suffit pas à qualifier ce lien.
