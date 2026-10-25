# HORIZON-FORMAT-001 — État de l'art des signatures documentaires et opportunité ULISTAG

**Référence : HORIZON-FORMAT-STATE-OF-ART-001**  
**Statut : étude conceptuelle rattachée à HORIZON-FORMAT-001**  
**Date d'instruction : 2026-10-18**

## Conclusion exécutive

La recherche conduite n'a pas identifié de **norme universelle unique** prescrivant une signature structurelle permettant de reconnaître tout modèle documentaire et de lui attribuer automatiquement un profil d'extraction. Cette conclusion est un **état de recherche documenté**, non une preuve absolue d'inexistence.

Les références existantes couvrent des couches différentes :

- PRONOM/DROID : identification du **format informatique** et de sa version par signatures binaires ou de conteneur ;
- Apache Tika : détection du **type de contenu / media type** et extraction de contenu ;
- ISO 15489 et ISO 23081 : principes de gestion des documents d'activité et de leurs métadonnées ;
- EN 16931-1:2026 : modèle sémantique des éléments d'une **facture électronique structurée** ;
- document layout analysis / OCR : lecture et segmentation de la structure visuelle ou textuelle ;
- moteurs à profils tels qu'invoice2data : sélection et extraction par règles/templates, sans standard universel de signature de modèle documentaire.

Aucune de ces briques ne couvre seule le contrat ULISDOQ :

`document privé local → signature observée → recherche de TAG → MATCH/AMBIGUOUS/UNKNOWN → profil d'extraction compatible → preuve de qualification`.

## Distinctions à préserver

- **Format informatique** : encodage/conteneur du fichier (PDF, PDF/A, OOXML, etc.).
- **Modèle documentaire** : organisation répétable d'un document métier ou éditorial.
- **Signature observée** : caractéristiques dérivées localement d'un document particulier.
- **TAG de format** : objet ULISDOQ versionné décrivant les critères de reconnaissance d'un modèle documentaire.
- **Identité de l'émetteur** : information distincte, facultative et révisable.
- **Profil d'extraction** : règles/champs attendus pour extraire des données.
- **Moteur compatible** : brique technique capable d'exécuter un profil.
- **Preuve de qualification** : corpus, protocole, versions, résultats, limites et décision.

## Cartographie de l'état de l'art

| Référence | Nature | Fonction réelle | Intégration locale | Limite pour ULISDOQ |
|---|---|---|---|---|
| PRONOM / DROID | Registre public + logiciel open source | Identifie précisément des formats de fichiers par extension, signatures binaires et signatures de conteneur ; associe des PUID | Oui ; DROID est une application Java locale, BSD-3-Clause | Reconnaît le format informatique, pas le modèle métier ou la mise en page d'une facture PDF |
| Apache Tika | Logiciel open source | Détecte un media type et extrait contenu/métadonnées via parsers | Oui ; Java, Apache-2.0 | Détection de type de contenu, pas attribution normalisée d'un profil documentaire |
| ISO 15489-1:2016 | Norme internationale | Concepts et principes de création, capture et gestion des documents d'activité | Applicable comme cadre documentaire | Ne définit pas de signature de layout ni d'algorithme de reconnaissance |
| ISO 23081-1:2017 / 23081-2:2021 | Normes internationales | Principes et cadre de métadonnées pour les documents d'activité et entités contextuelles | Applicable comme cadre de métadonnées | Ne spécifie pas un matcher universel de modèles documentaires |
| EN 16931-1:2026 | Norme européenne | Modèle sémantique des éléments de base d'une facture électronique | Pertinent pour normaliser la sémantique des factures structurées | Ne reconnaît pas la mise en page d'un PDF arbitraire ; ce n'est pas une signature visuelle |
| pdfplumber | Bibliothèque open source MIT | Extrait localement texte, caractères, mots, lignes, rectangles, tables et coordonnées depuis des PDF, surtout natifs | Oui ; Python | Lecteur structuré, pas matcher ni standard de signature |
| LayoutParser | Bibliothèque open source Apache-2.0 | Analyse de layout assistée par modèles de deep learning | Oui, avec dépendances modèles | Plus lourd ; la robustesse dépend du domaine et des modèles ; ne fournit pas le contrat ULISDOQ |
| docTR | Bibliothèque open source Apache-2.0 | OCR : localisation et reconnaissance de texte dans les documents | Oui ; Python / PyTorch | OCR, pas attribution canonique TAG→profil |
| invoice2data | Logiciel open source MIT | Sélectionne des templates via mots-clés/exclusions puis extrait des champs par règles | Oui ; Python/CLI | Offre déjà un matching de templates utile, mais centré factures et lié à son modèle de template ; pas un standard transversal |

### Niveau de normalisation

- **Normes officielles** : ISO 15489, ISO 23081, EN 16931.
- **Registre / spécification technique institutionnelle** : PRONOM et syntaxe de signatures DROID.
- **Standards de fait / interfaces logicielles** : Apache Tika et mécanismes des bibliothèques documentaires.
- **Implémentations open source** : DROID, Tika, pdfplumber, LayoutParser, docTR, invoice2data.

Les textes normatifs ISO/EN restent soumis aux conditions de diffusion des organismes de normalisation ; leur existence et leur périmètre peuvent être référencés sans considérer leur texte intégral comme librement réutilisable.

## Lacune réellement non couverte

La lacune pertinente pour ULISDOQ n'est **pas** l'absence de lecteurs, d'OCR, de moteurs de layout ou de mécanismes de template matching. Ces briques existent.

La lacune est un **contrat interopérable et transversal** permettant de :

1. décrire une signature observée sans exposer le document privé ;
2. comparer cette signature à un catalogue versionné de TAGs de modèles documentaires ;
3. produire un résultat explicite `MATCH | AMBIGUOUS | UNKNOWN` avec critères et preuves ;
4. résoudre un TAG vers un ou plusieurs profils d'extraction versionnés et leurs moteurs compatibles ;
5. conserver provenance, versions, seuils, limites et statut de qualification ;
6. contribuer un TAG candidat sans faire de sa publication une qualification.

## Opportunité ULISTAG

**Décision : opportunité confirmée comme désignation candidate interne à HORIZON-FORMAT-001 ; pas de projet indépendant et pas de moteur imposé.**

ULISTAG est le plus utile s'il désigne d'abord un **contrat ouvert de représentation et d'échange**, utilisable par plusieurs lecteurs et matchers. Une bibliothèque, une CLI ou une interface graphique peuvent ensuite implémenter ce contrat sans en devenir la définition canonique.

Le contrat doit rester modulaire :

```text
LECTEUR LOCAL
    ↓
SIGNATURE OBSERVÉE
    ↓
MOTEUR DE COMPARAISON SUBSTITUABLE
    ↓
TAG ULISDOQ
    ↓
MAPPING TAG → PROFIL(S)
    ↓
MOTEUR(S) D'EXTRACTION COMPATIBLE(S)
```

## Contrat minimal interopérable candidat

### Signature observée

- `schema_version`
- `reader.component_id`
- `reader.version`
- `document_media_type`
- `page_count`
- caractéristiques textuelles **non sensibles** normalisées
- caractéristiques géométriques optionnelles
- caractéristiques visuelles optionnelles
- provenance locale de l'observation
- `privacy_review`
- empreinte du descripteur canonisé, distincte du hash du document privé

### TAG de format

- `tag_id`
- `version`
- `status = CANDIDATE | TESTED | QUALIFIED | REJECTED | WITHDRAWN`
- `family`
- critères de reconnaissance
- seuils / tolérances
- périmètre de validité
- corpus/protocole de qualification
- preuves et limites

### Résultat de correspondance

- `status = MATCH | AMBIGUOUS | UNKNOWN`
- `tag_candidates[]`
- score ou critères satisfaits lorsque le moteur en produit
- explication bornée des critères
- version du catalogue et du moteur de comparaison
- `profile_refs[]` seulement via une liaison TAG→profil explicite

Le contrat ne doit pas imposer qu'un score numérique existe : un matcher déterministe à règles peut être valable.

## Méthode de qualification

Évaluer chaque TAG/matcher sur :

- positifs indépendants ;
- variantes réelles ;
- négatifs proches et lointains ;
- faux positifs et faux négatifs ;
- cas ambigus et inconnus ;
- changements de layout ;
- indices trompeurs ;
- répétabilité ;
- coût de calcul ;
- confidentialité des descripteurs ;
- compatibilité réelle du profil et du moteur d'extraction.

Les dérivés d'un même original ne constituent pas des échantillons indépendants pour démontrer la généralisation d'un TAG.

## Expérience bornée suivante — GED-01 / source originale

Le cas disponible est adapté à une première verticale **sans développement prématuré d'un nouveau moteur** :

1. utiliser localement `pdfplumber 0.11.10` sur la facture originale ;
2. produire une signature observée minimisée à partir de caractéristiques structurelles non sensibles ;
3. définir un TAG candidat correspondant au modèle déjà étudié dans GED-01 ;
4. évaluer d'abord les mécanismes existants de sélection de template d'`invoice2data` comme matcher de référence ;
5. si nécessaire seulement, ajouter un comparateur ULISDOQ minimal ;
6. vérifier que la correspondance conduit au profil `experiences/factures/GED-01/modeles/fournisseur_exp_01.yml` ;
7. exécuter ce profil localement sur la source originale et vérifier les champs attendus ;
8. qualifier séparément :
   - la compatibilité du profil avec cette source originale ;
   - la capacité de reconnaissance du TAG, qui exige ensuite des positifs indépendants et des négatifs.

Le document original et les extractions contenant des données personnelles restent hors du dépôt.

## Sources de référence

- The National Archives — PRONOM / DROID : https://www.nationalarchives.gov.uk/information-management/manage-information/preserving-digital-records/droid/
- PRONOM — DROID Signature Files : https://pronom.nationalarchives.gov.uk/signature-list
- DROID source et syntaxe : https://github.com/digital-preservation/droid
- Apache Tika — Content Detection : https://tika.apache.org/3.2.1/detection.html
- ISO 15489-1:2016 : https://www.iso.org/standard/62542.html
- ISO 23081 : https://committee.iso.org/sites/tc46sc11/home/projects/published/iso-23081-metadata-for-records.html
- Commission européenne — EN 16931-1:2026 : https://ec.europa.eu/digital-building-blocks/sites/spaces/DIGITAL/pages/467108971/Obtaining+a+copy+of+the+European+standard+on+eInvoicing
- pdfplumber : https://github.com/jsvine/pdfplumber
- LayoutParser : https://layout-parser.github.io/
- docTR : https://mindee.github.io/doctr/
- invoice2data : https://github.com/invoice-x/invoice2data
