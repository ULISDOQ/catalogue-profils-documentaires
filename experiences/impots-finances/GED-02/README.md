# GED-02 — Formulaire 2044 et connaissance officielle associée

**Statut : expérience phase 1 — PASS_CANDIDATE technique, non qualifiée.**

GED-02 suit la [méthode GED-N phase 1](../../../ULISTAG/protocols/PHASE1_GED_CASE_METHOD.md). Le corpus synthétique comporte huit variantes positives du formulaire 2044 étudié et un témoin négatif fiscal ressemblant. Une première méthode ULISTAG spécialisée, fondée sur la densité de mise en page multi-pages, sépare les huit positifs du négatif sur ce corpus.

Voir :
- [méthode ULISTAG GED-02](ulistag/LAYOUT_DENSITY_V0_1.md) ;
- [résultats v0.1](ulistag/RESULTS_V0_1.md) ;
- [référence v0.1](ulistag/reference_layout_density_v0_1.json) ;
- [matcher expérimental](ulistag/layout_density_v0_1.py).

Ce succès est un résultat de **phase 1** : il justifie la poursuite horizontale des GED-N, pas une qualification de production.

GED-02 utilise le **formulaire 2044 — déclaration des revenus fonciers** comme cas concret pour éprouver une capacité fondatrice d'ULISDOQ : partir d'un document administratif identifiable et le relier à la connaissance officielle publiée qui le décrit, l'explique et le situe dans une version précise.

L'extraction n'est pas le cœur premier de cette expérience.

## Sources déjà identifiées pour le cas 2044

### impots.gouv.fr

Page officielle du formulaire 2044 :

https://www.impots.gouv.fr/formulaire/2044/declaration-des-revenus-fonciers

Cette source permet de travailler sur :

- l'intitulé officiel ;
- le formulaire publié ;
- les millésimes disponibles ;
- les notices associées ;
- les variantes ou formulaires voisins.

Elle peut servir de référence pour distinguer une simple ressemblance documentaire d'une **identité documentaire datée et sourcée**.

### Service-Public.gouv.fr

Fiche publique du formulaire 2044 :

https://www.service-public.gouv.fr/particuliers/vosdroits/R1283

La fiche permet de relier le formulaire à son identité administrative, son usage, son ministère émetteur et ses ressources associées. Elle fait également apparaître des relations avec des formulaires ou notices voisins, notamment les variantes de la famille 2044.

### BOFiP

https://bofip.impots.gouv.fr/

Le BOFiP fournit la doctrine administrative permettant de comprendre **dans quel contexte fiscal utiliser la 2044 et comment elle se distingue de variantes comme la 2044-SPE**.

Cette couche est importante pour ULISDOQ : deux documents visuellement ou lexicalement proches peuvent relever de règles d'usage différentes.

### Légifrance

https://www.legifrance.gouv.fr/

Légifrance peut compléter la qualification lorsqu'un texte réglementaire ou législatif permet d'établir l'origine normative, la période de validité ou le cadre juridique du document.

## ULISTAG phase 1

GED-02 dispose désormais d'un candidat de reconnaissance structurelle de phase 1 fondé sur le matcher réutilisable [visual_keypoints](../../../ULISTAG/matchers/visual_keypoints/README.md).

La référence est construite à partir du PDF officiel `2044_5132.pdf` puis stabilisée avec une première représentation synthétique S01. Le même TAG candidat est ensuite éprouvé successivement sur S02 à S08, puis sur un témoin négatif fiscal ressemblant.

Résultat expérimental :

```text
S01..S08 = MATCH_CANDIDATE
N01       = UNKNOWN
QUALIFICATION = NONE
```

Voir [l'expérience ULISTAG GED-02](ulistag/PHASE1_2044_VISUAL_KEYPOINTS_V0_1.md) et le [manifest de construction reproductible](ulistag/reference_visual_v0_1_manifest.json).

Cette réussite reste un résultat de **phase 1** : elle sert à éprouver une méthode industrialisable de fabrication des GED-N, non à produire dès maintenant un TAG définitif ou une qualification de production.

## Profil candidat

Le profil candidat est [profiles/fr_formulaire_2044_candidate.json](profiles/fr_formulaire_2044_candidate.json).

Il ne doit pas être considéré comme qualifié du seul fait que le numéro « 2044 » ou l'expression « revenus fonciers » sont reconnus.

Les versions annuelles, annexes et variantes doivent être distinguées à partir de sources officielles datées.

## Chaîne de connaissance recherchée

```text
document / caractéristiques observées
→ candidat « formulaire 2044 »
→ référence officielle impots.gouv.fr
→ identité et contexte Service-Public
→ millésime / notice / variantes
→ doctrine BOFiP pertinente
→ texte normatif si nécessaire
→ connaissance documentaire sourcée
→ éventuel profil technique
```

## Trois qualifications distinctes

**Qualification identitaire** : établir qu'il s'agit bien d'un formulaire 2044 déterminé, avec son numéro administratif, sa version ou son millésime et sa source officielle.

**Qualification sémantique** : relier ce formulaire à son usage, sa notice, ses variantes et aux connaissances publiques qui expliquent son emploi.

**Qualification technique** : déterminer si ULISDOQ sait reconnaître ce modèle, lui associer un TAG ou ULISTAG, sélectionner un profil et en extraire correctement les informations.

Ces trois niveaux ne doivent pas être confondus.

## Ce que doit démontrer GED-02

GED-02 doit montrer qu'ULISDOQ sait :

1. caractériser suffisamment un document administratif ;
2. retrouver la référence officielle correspondante ;
3. établir un lien sourcé entre document, version et connaissance publiée ;
4. distinguer les variantes et millésimes ;
5. conserver les distinctions entre document, source de connaissance, TAG, profil et moteur ;
6. signaler `UNKNOWN` ou `AMBIGUOUS` lorsque la correspondance n'est pas suffisamment établie.

Le TAG peut être préparé localement avec l'[éditeur ULISDOQ](../../../client/tag_candidate.py), mais **l'extraction vient après la qualification documentaire**.

Aucun document fiscal personnel réel n'est requis dans le dépôt pour conduire cette expérimentation.


## Clôture phase 1 et reprise phase 2

La phase 1 GED-02 est désormais considérée comme **concluante et suffisante pour poursuivre vers GED-N+1**, sans qualification production du profil 2044.

Le package canonique de reprise phase 2 est :

- [phase2-reentry/README.md](phase2-reentry/README.md)
- [phase2-reentry/SOURCE_MANIFEST_V0_1.json](phase2-reentry/SOURCE_MANIFEST_V0_1.json)
- [phase2-reentry/evidence/S11_PROFILE_DRIVEN_EXTRACTED_FROZEN.json](phase2-reentry/evidence/S11_PROFILE_DRIVEN_EXTRACTED_FROZEN.json)
- [phase2-reentry/evidence/S11_DGFIP_SYNTHETIC_GROUND_TRUTH.json](phase2-reentry/evidence/S11_DGFIP_SYNTHETIC_GROUND_TRUTH.json)
- [profiles/DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001.md](profiles/DEBT-GED02-PROFILE-SEMANTIC-ROBUSTNESS-001.md)

Règle de reprise : **ne pas repartir de zéro**. Reprendre l'implémentation et les preuves existantes, traiter les deltas explicitement inscrits dans la dette, puis qualifier si et seulement si les preuves deviennent suffisantes.
