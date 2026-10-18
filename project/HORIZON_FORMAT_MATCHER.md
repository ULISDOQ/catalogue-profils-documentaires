# Horizon ULISDOQ — Reconnaissance et qualification des formats documentaires

**Référence : HORIZON-FORMAT-001**  
**Statut : HORIZON DÉCLARÉ — ARCHITECTURE CONCEPTUELLE CANDIDATE**  
**Principe : simplicité, interopérabilité, lisibilité et prudence juridique.**

## Intention

Permettre à un logiciel consommateur de retrouver automatiquement, parmi les profils ULISDOQ, celui qui convient à un document entrant, puis d'en exploiter les règles d'extraction **localement et sans appel à ChatGPT**. La métaphore « Shazam du format documentaire » désigne une capacité de reconnaissance de **mise en forme**, non d'identification de la personne ou du contenu privé.

Ce chantier est un **horizon déclaré**, non une capacité existante ou une obligation d'inventer un moteur. L'évaluation des mécanismes de reconnaissance des briques techniques référencées est préalable à toute nouvelle implémentation. La sélection d'une brique compatible dépend des capacités requises et des preuves disponibles, et non d'un moteur imposé. Voir aussi [l'architecture des identités canoniques](HORIZON_IDENTITY_MAPPING.md).

L'[éditeur local de TAG candidat](TAG_CANDIDATE_PROTOCOL.md) est un premier démonstrateur borné : il ne réalise pas encore la recherche de correspondances.

## Architecture conceptuelle

```text
                     CONSTRUCTION / QUALIFICATION (hors production)
Corpus autorisé (positifs, variantes, négatifs)
        │
        ▼
Analyse de stabilité : texte OCR + géométrie + repères visuels
        │
        ▼
TAG de format candidat ───► épreuves sur corpus indépendant
        │                              │
        │                     métriques + limites + revue
        │                              │
        └──────────────────────────────▼
                   Registre ULISDOQ versionné (Git)
              TAG ──associe──► profil d'extraction
                       │       + tests + preuves
                       │
                       ▼
                    CONSOMMATEUR
API GitHub ──► synchronisation contrôlée ──► cache local épinglé
                                              │
Document privé entrant ─► lecteur local ─► signature observée
                                              │
                                              ▼
                                     comparaison aux TAGs
                                     / sélection de candidats
                                              │
                               ┌──────────────┴──────────────┐
                               ▼                             ▼
                     correspondance qualifiée        inconnu / ambigu
                               │                             │
                               ▼                             ▼
                        profil compatible              refus explicite
                               │                        / revue hors flux
                               ▼
                   OCR + moteur d'extraction local
                               │
                               ▼
                      extraction structurée
                               │
                               ▼
                  contrôles métier et traçabilité
                               │
                               ▼
                       GED / client local
```

## Objets distincts

| Objet | Responsabilité |
|---|---|
| **Document entrant** | Document privé du consommateur ; ne quitte pas son environnement. |
| **Signature observée** | Descripteurs dérivés localement d'un document ; ne pas publier sans examen de confidentialité. |
| **TAG de format** | Identifiant stable, version, indices discriminants, tolérances, seuils et limites ; indépendant des valeurs de facture. |
| **Profil d'extraction** | Règles versionnées et moteur d'extraction compatible. |
| **Liaison TAG → profil** | Référence explicite et versionnée ; un TAG peut désigner plusieurs profils candidats. |
| **Preuve de qualification** | Corpus caractérisé, protocole, versions, résultats, métriques, limites et décision. |
| **Client consommateur** | Télécharge et épingle les versions approuvées ; reconnaît, extrait, contrôle et journalise localement. |

**Reconnaître un format ≠ extraire les données ≠ valider les données.** Une bonne reconnaissance ne garantit pas une extraction correcte.

## Stratégie de construction : réemployer avant d'inventer

1. Évaluer la reconnaissance native d'un moteur existant (mots-clés, modèles, règles) sur un corpus expérimental.
2. Caractériser les échecs réels : confusion entre formats, variantes de mise en page, OCR, refus.
3. Ajouter seulement les descripteurs nécessaires : positions relatives, structure de page, zones stables, repères visuels. Ne pas utiliser les montants, identifiants clients ou dates comme signature d'identité du format.
4. Comparer les approches sur **les mêmes corpus indépendants**, et retenir la plus simple satisfaisant les critères.
5. Ne prévoir un modèle appris ou un index vectoriel que si une insuffisance mesurée justifie ce coût.

## Qualification sur corpus

- **Positifs** : plusieurs factures authentiquement différentes du même format, sur différentes périodes et si possible différents comptes, avec consentement et droits appropriés.
- **Variantes** : pages supplémentaires, scans, résolutions, décalages, nouveaux montants et dates ; les copies artificiellement modifiées restent identifiées comme telles.
- **Négatifs** : autres fournisseurs et autres variantes du même fournisseur.
- **Séparation stricte** : construction/réglage d'un côté ; validation indépendante de l'autre. Des dérivés d'un même original restent dans le même groupe pour éviter une fuite statistique.
- **Mesures** : précision, rappel, faux positifs, taux d'inconnus/ambigus, robustesse et temps/coût de calcul.
- **Décision** : TAG CANDIDATE → TESTED → QUALIFIED pour un périmètre borné, ou REJECTED / WITHDRAWN. Pas de qualification par simple présence dans Git.

Le nombre de factures requis dépend de la diversité des formats et des résultats observés ; aucun volume arbitraire ne garantit la fiabilité.

## Contrat d'interopérabilité visé

- Catalogue Git public versionné ; profil et TAG récupérables par **API GitHub ou Git**, avec identifiants et empreintes vérifiables.
- Descriptions lisibles et sérialisables dans des formats ouverts (JSON/YAML) ; schéma stable et documenté, sans dépendance à un logiciel consommateur.
- Cache local, version épinglée, politique de mise à jour explicite ; **aucune promotion automatique** d'un TAG non qualifié.
- Aucune facture de production transmise à GitHub/ULISDOQ ; aucune requête à ChatGPT nécessaire au chemin nominal.
- Échec fermé en cas de format inconnu, score insuffisant, conflit entre profils ou contrôles d'extraction échoués.
- Les briques de lecture, d'OCR, de reconnaissance, d'extraction et de validation restent substituables selon leurs contrats de compatibilité. La reconnaissance du format ne suppose pas l'identification de l'entité émettrice.

## Prudence juridique et publication

Conserver les factures privées dans le SI autorisé. Publier préférentiellement TAGs, profils, protocoles et résultats agrégés non identifiants ; ne publier des exemples que si leur confidentialité et leurs droits de redistribution ont été examinés. Une signature peut elle-même révéler des informations et doit être contrôlée. Prévoir signalement et retrait rapide d'un contenu contesté.

## Première étape bornée

**GED-01** : faire fonctionner le profil d'extraction candidat, observer ses erreurs, réunir un corpus de factures indépendantes et de contre-exemples, puis décider **si un TAG graphique ajoute réellement de la valeur**. Pas de développement d'un nouveau moteur avant cette décision.

## Non-objectifs à ce stade

Pas d'entraînement de LLM, pas d'API centralisée recevant les factures, pas de classement de personnes, pas de garantie universelle de reconnaissance, pas de certification de performance avant tests indépendants.
