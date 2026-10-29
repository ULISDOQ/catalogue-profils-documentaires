# Factures & achats — famille documentaire

Cette famille regroupe les expériences ULISDOQ consacrées aux **factures, achats, reçus et documents fournisseurs**, indépendamment d'un fournisseur, d'un moteur ou d'un modèle particulier.

**Objectif pour les relecteurs :** montrer comment un document de cette famille peut être reconnu, rapproché d'un profil partageable, traité localement et qualifié sans transmettre le document privé à ULISDOQ.

## Cycle commun

Les expériences de cette famille servent à éprouver progressivement le cycle :

```text
document local
→ lecture / caractérisation
→ reconnaissance du modèle documentaire
→ TAG / empreinte structurelle
→ profil d'extraction candidat
→ moteur compatible
→ extraction
→ contrôles
→ qualification bornée
```

**Reconnaître un format, sélectionner un profil, extraire des données et valider le résultat sont des opérations distinctes.**

Un profil de facture n'est pas qualifié par sa seule présence dans le dépôt. Sa qualification doit préciser le modèle documentaire couvert, les versions, le moteur utilisé, le corpus d'épreuve, les contrôles, les limites et les preuves.

## Séparation des identités, formats et profils

Une organisation, un modèle de facture et un profil d'extraction sont des objets distincts.

Le nom commercial d'un émetteur ne constitue ni l'identité canonique d'un profil ni une preuve suffisante de reconnaissance. Un même émetteur peut produire plusieurs modèles ; plusieurs émetteurs peuvent partager un modèle proche ; un même modèle peut disposer de plusieurs profils selon les moteurs compatibles.

L'architecture canonique est décrite dans [HORIZON_IDENTITY_MAPPING.md](../../documentation/architecture/IDENTITES_CORRESPONDANCES.md).

## Ce que doit apporter ULISDOQ

ULISDOQ publie et versionne les éléments partageables nécessaires au traitement local :

- TAGs ou empreintes de référence ;
- profils d'extraction ;
- compatibilités avec les moteurs ;
- fixtures autorisées ;
- protocoles de test ;
- preuves et limites de qualification.

ULISDOQ **ne reçoit pas les factures de production**. Le document privé reste chez le consommateur, qui récupère une version précise des ressources ULISDOQ et exécute localement les traitements compatibles.

```text
document privé local
→ ressources ULISDOQ versionnées
→ reconnaissance / sélection
→ moteur local compatible
→ extraction structurée
→ contrôles du consommateur
→ système cible
```

## Réutilisation opérationnelle cible

Une fois un profil **qualifié dans un périmètre explicite**, un consommateur peut :

- récupérer une version immuable ou épinglée du profil et de ses références ;
- vérifier leur identité et leur compatibilité ;
- les conserver en cache local ;
- traiter de nouveaux documents sans transmettre leur contenu à ULISDOQ ;
- refuser explicitement un format inconnu, ambigu ou non qualifié ;
- ouvrir un travail de qualification lorsqu'un nouveau modèle apparaît.

Aucune mise à jour non qualifiée ne doit être promue automatiquement dans un chemin de production.

## Confidentialité et publication

Les documents privés de production restent chez le consommateur.

Les fixtures publiées doivent être autorisées, identifiées comme expérimentales lorsque nécessaire et examinées au regard de la confidentialité et des droits de diffusion. Une version modifiée ou dérivée d'un document réel ne doit pas être présentée comme un original authentique ni comme une preuve automatique d'anonymisation.

Pour contribuer : proposer un profil, une fixture autorisée, un TAG candidat, une exécution reproductible, une preuve de qualification ou une critique précise ; ne pas déposer de facture personnelle brute.

## Organisation

Chaque sous-dossier `GED-NN/` est une expérience bornée portant sur un cas particulier. Il contient ses propres fixtures, profils ou templates, tests et preuves.

Le client générique ULISDOQ reste dans [`/client`](../../logiciels/client/README.md) : une expérience utilise le client mais n'en est pas propriétaire.

## Expériences

- [GED-01 — Une facture, un profil, un résultat](GED-01/README.md) : première expérience de profil de facture et de rapprochement avec une source réelle conservée localement.

D'autres expériences de factures pourront être ajoutées ici sans modifier le contrat général de la famille.
