# ULISDOQ — Architecture horizontale des identités et des formats

**Référence : HORIZON-IDENTITY-001**  
**Statut : architecture conceptuelle candidate, non implémentée**  
**Dimensionnement de référence : 88 821 entités (objectif, pas inventaire existant)**

## Doctrine

Le catalogue est **agnostique des marques et des métiers**. Le nom d'une organisation n'est ni l'identité d'un profil, ni une condition nécessaire à l'extraction. Les marques, dénominations, sigles et autorités administratives appartiennent à un **référentiel de correspondance**, indépendant des règles de lecture documentaire. Les noms propres éventuels sont cantonnés aux expériences unitaires et aux enregistrements du référentiel, jamais aux principes architecturaux généraux.

Une entité, un format et un profil sont trois objets distincts. Une entité peut émettre plusieurs formats ; un format peut être partagé par plusieurs entités ; un format peut disposer de plusieurs profils adaptés à des moteurs différents.

## Graphe conceptuel

```text
   Référentiel des entités (dimensionnement cible : 88 821)
      ENTITY-ID canonique ── alias / marques / dénominations
                │
                │ relations datées, sourcées, non exclusives
                ▼
      Correspondances entité ↔ format
                ▲
                │
Document local → signature observée → TAG-FORMAT-ID
                                         │
                                         ▼
                               PROFILE-ID + VERSION
                                         │
                                         ▼
                           moteur d'extraction local
                                         │
                                         ▼
                            champs normalisés + preuves
```

## Contrats d'objet minimaux

- **ENTITY-ID** : identifiant ULISDOQ stable et opaque, type (organisation commerciale, administration, établissement, etc.), identifiants publics externes optionnels, statut et provenance ; aucun nom encodé dans la clé.
- **ENTITY-ALIAS** : dénomination ou marque, type d'alias, langue, période de validité, source et niveau de confiance ; homonymies possibles.
- **FORMAT-ID / TAG** : famille, version, caractéristiques de reconnaissance textuelles ou géométriques, seuils, périmètre de validité et preuves ; indépendant de l'identité juridique de l'émetteur.
- **PROFILE-ID / VERSION** : schéma des champs, règles d'extraction, moteur compatible, tests et statut de qualification ; sans nom de marque obligatoire.
- **MAPPING** : liens plusieurs-à-plusieurs entre entités, formats et profils, avec origine, période, confiance et décision de revue.
- **RESULT** : document traité localement, format/profil retenus, version et preuves, données extraites, contrôles, et identité émetteur uniquement si elle est établie séparément.

## Règles d'identification

1. Reconnaître d'abord **le format documentaire** ; l'identification de l'émetteur est un enrichissement distinct, facultatif et révisable.
2. Ne jamais déduire une identité certaine du seul aspect graphique, d'un logo ou d'un nom OCR : produire des candidats avec provenance et confiance.
3. Permettre `UNKNOWN` et `AMBIGUOUS` ; refuser toute correspondance non suffisamment étayée.
4. Ne pas transmettre de documents privés au référentiel ; distribuer ses index versionnés pour la recherche locale.
5. Utiliser des identifiants canoniques opaques plutôt que des noms de marques dans les contrats d'interopérabilité.
6. Éviter le catalogue géant de copies : mutualiser les formats et les profils ; versionner les liens d'entités séparément.

## Portabilité des moteurs

Un moteur externe peut imposer un champ technique `issuer` ou des mots-clés de sélection. Cet adaptateur reste **une contrainte du moteur**, pas la définition canonique de l'entité. Si nécessaire, générer un gabarit technique avec un identifiant opaque, ou sélectionner explicitement le profil avant extraction. Ne pas présumer que tout moteur reconnaît un format sans indices discriminants.

## Qualification et échelle

Les **88 821 entités** représentent un **horizon de dimensionnement** demandé, sans prétendre que les entités sont recensées, uniques ou qualifiées. Un catalogue à cette échelle nécessite une politique de dédoublonnage, des identifiants pérennes, des sources légitimes, un suivi des changements de nom et des tests de performance d'indexation. Le nombre d'entités n'est pas le nombre de formats ni le nombre de profils.

L'horizontalité doit être démontrée sur des documents de plusieurs familles et organisations, par des mesures de reconnaissance, extraction, faux positifs, ambiguïtés et coût de calcul, et non par une simple taille de référentiel.

## Expérience initiale

GED-01 utilise provisoirement `Fournisseur-EXP-01` comme **alias de démonstration uniquement**. Les images restent des pièces expérimentales ; aucune entité réelle n'est inscrite comme identité canonique. Les noms commerciaux visibles sur une image ne prouvent pas une affiliation ni une qualification.
