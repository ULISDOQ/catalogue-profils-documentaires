# ULISDOQ — Architecture horizontale des identités et des formats

**Référence : HORIZON-IDENTITY-001**  
**Statut : architecture conceptuelle candidate, non implémentée**  

## Doctrine

Le catalogue est **agnostique des marques et des métiers**. Le nom d'une organisation n'est ni l'identité d'un profil, ni une condition nécessaire à l'extraction. Les marques, dénominations, sigles et autorités administratives appartiennent à un **référentiel de correspondance**, indépendant des règles de lecture documentaire. Les noms propres éventuels sont cantonnés aux expériences unitaires et aux enregistrements du référentiel, jamais aux principes architecturaux généraux.

Une entité, un format et un profil sont trois objets distincts. Une entité peut émettre plusieurs formats ; un format peut être partagé par plusieurs entités ; un format peut disposer de plusieurs profils adaptés à des moteurs différents.

## Graphe conceptuel

```text
   Référentiel des entités (échelle ouverte)
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

## Unification des briques techniques

Le profil référence des capacités requises ; un registre distinct relie ces capacités à N briques techniques versionnées, compatibles et qualifiées dans un périmètre explicite. Voir [UNIFICATION_TECHNICAL_COMPONENTS.md](UNIFICATION_COMPOSANTS_TECHNIQUES.md).

## Portabilité des moteurs

Un moteur externe peut imposer un champ technique `issuer` ou des mots-clés de sélection. Cet adaptateur reste **une contrainte du moteur**, pas la définition canonique de l'entité. Si nécessaire, générer un gabarit technique avec un identifiant opaque, ou sélectionner explicitement le profil avant extraction. Ne pas présumer que tout moteur reconnaît un format sans indices discriminants.

## Qualification et échelle

L'échelle d'ULISDOQ ne se mesure pas au nombre d'organisations ou d'entités référencées, mais à sa capacité à **mutualiser des modèles documentaires réellement réutilisables** et à les relier à des profils qualifiés.

Une organisation peut produire plusieurs modèles documentaires ; inversement, un même modèle ou une même famille de profils peut être utile à de nombreuses organisations. Le nombre d'entités, le nombre de formats et le nombre de profils sont donc trois grandeurs distinctes.

La question utile devient :

```text
combien de profils documentaires qualifiés
faut-il pour couvrir une part donnée
du volume documentaire réellement rencontré ?
```

Cette question est traitée plus directement dans l'[étude de faisabilité sur la couverture documentaire de 1 000 organisations](../etudes/ETUDE_FAISABILITE_COUVERTURE_PROFILS_1000_ORGANISATIONS.md), qui pose une première hypothèse de dimensionnement et surtout propose comme indicateur principal le **taux de documents couverts par des profils qualifiés**, plutôt que la taille brute du catalogue.

L'horizontalité doit être démontrée sur plusieurs familles documentaires et plusieurs organisations, avec des mesures de reconnaissance, d'ambiguïté, d'inconnus, d'extraction, de réutilisation inter-organisations et de coût de qualification. Une grande quantité d'entités ou de profils présents dans le dépôt ne constitue pas en elle-même une preuve de couverture ni de qualité.

## Expérience initiale

GED-01 utilise provisoirement `Fournisseur-EXP-01` comme **alias de démonstration uniquement**. Les images restent des pièces expérimentales ; aucune entité réelle n'est inscrite comme identité canonique. Les noms commerciaux visibles sur une image ne prouvent pas une affiliation ni une qualification.
