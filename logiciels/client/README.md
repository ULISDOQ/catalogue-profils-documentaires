# Client ULISDOQ — rôle, capacités et travaux restants

Le rôle visé du client est d'**exploiter localement des profils existants pour remettre des données structurées et contrôlées à un logiciel consommateur**. Le Profile Builder aide à fabriquer un profil candidat ; le client doit permettre son exploitation ultérieure sans repasser par sa fabrication.

**Aujourd'hui, ce dossier rassemble plusieurs commandes candidates, pas un client unifié.** Il ne sait pas recevoir un document quelconque, choisir automatiquement tout profil du catalogue puis en exécuter le traitement. Aucun profil ni chaîne complète n'est qualifié pour la production.

## Distinguer les objets

| Objet | Fonction | Exemple |
| --- | --- | --- |
| Brique technique | Lire, reconnaître, extraire ou valider | invoice2data, Tesseract, parseur EML, matcher ULISTAG |
| Adaptateur | Rendre une brique appelable selon une interface maîtrisée | [extract.py](extract.py), interface locale vers invoice2data |
| Profil documentaire | Décrire un traitement applicable, ses champs, ressources, contraintes et compatibilités | Profil JSON ou modèle YAML compatible avec un moteur donné |
| Client | Sélectionner et appliquer les ressources compatibles, contrôler et restituer les résultats | Aujourd'hui : commandes séparées ; à terme : chaîne d'exploitation |
| [Profile Builder](../profile-builder/README.md) | Aider à fabriquer et éprouver un profil candidat | Aujourd'hui : sélection de capacités et plan de traitement, sans exécution des moteurs ni matérialisation de profil |

Un profil validé n'est donc pas une nouvelle brique logicielle. L'objectif est de réutiliser N briques compatibles pour exploiter les profils adaptés. La qualification d'un profil ne le rend pas compatible avec n'importe quel moteur.

Le registre du Builder référence déjà les adaptateurs de ce dossier. Fabrication et exploitation peuvent réemployer les mêmes capacités ; leur code ne doit pas être dupliqué.

## Ce que le dossier produit aujourd'hui

| Programme | Entrées à fournir | Sortie réelle | Limite actuelle |
| --- | --- | --- | --- |
| [Adaptateur invoice2data](extract.py) | Facture, répertoire de modèles YAML et lecteur | Contrat : JSON `EXTRACTED_UNVERIFIED`, `NO_MATCH` ou `ERROR`, données si extraction et empreinte source | Spécialisé dans les factures compatibles invoice2data. Chargement corrigé par B ; extraction encore bloquée par le défaut de lecteur réservé à C. |
| [Extraction de courriel](eml_extract_v0_1.py) | Fichier EML, profil et schéma | JSON : statut de lecture, en-têtes, adresses, texte, présence HTML, métadonnées des pièces jointes et traçabilité | Neuf cas synthétiques GED-03 éprouvés. Pas d'exécution ou d'interprétation sémantique générale des pièces jointes. |
| [OCR piloté par profil](profile_ocr_extract_v0_1.py) | PDF, registre, TAG déjà choisi, profil/binding référencés et schéma | JSON de champs : valeurs ou statuts `UNREADABLE`/`AMBIGUOUS`, preuves et empreintes | Primitive éprouvée sur fixture synthétique. Le TAG est fourni, pas reconnu automatiquement ; la dette d'exactitude GED-02 reste ouverte. |
| [Résolveur de profils](profile_resolver_v0_1.py) | Registre local, type MIME et extension déclarés | JSON `MATCH`, `UNKNOWN` ou `AMBIGUOUS`, nombre et références des candidats | Mode `CONTAINER_NATIVE` seulement. Ne lit pas le document et ne contrôle pas la qualification de production. |
| [Éditeur de TAG candidat](tag_candidate.py) | Famille et indices saisis, géométrie optionnelle | Fichier JSON, identifiant et empreinte ; `CANDIDATE_UNQUALIFIED`, `NOT_CHECKED` | Préparation d'une ressource, pas exploitation d'un document ni reconnaissance. Voir le [protocole](documentation/PROTOCOLE_TAG_CANDIDAT.md). |

Les sorties ne partagent pas encore une enveloppe commune. Une extraction ou une conformité au schéma ne prouve pas l'exactitude des données. Les sorties peuvent contenir les données privées du document et restent dans l'environnement autorisé du consommateur.

Les expériences GED sont des cas d'épreuve ; elles ne définissent pas les limites du logiciel. En particulier, l'adaptateur invoice2data reçoit ses chemins en arguments, sans imposer GED-01.

## Superpositions actuelles à examiner

Le nom « client » rassemble aujourd'hui trois responsabilités : adaptateurs d'exécution, résolution de ressources et préparation d'un TAG candidat. L'éditeur de TAG relève de la préparation documentaire ; sa présence ici ne signifie pas qu'il fait partie du traitement nominal d'un consommateur.

Le client et le Builder ont besoin de capacités communes. Le futur enchaînement d'exécution ne doit pas dupliquer le planner du Builder, les moteurs ou les règles des profils. La frontière entre bibliothèque réutilisable et commandes utilisatrices reste à préciser.

Ces constats appellent une décision architecturale. Cette page **ne décide aucun déplacement, fusion ou création de sous-projet** ; elle rend le mélange actuel et les dépendances visibles.

## Horizon phase 3

La [stratégie des trois phases](../../documentation/architecture/GED_CORE_MACHINE_PROFILE_BUILDER_ARCHITECTURE_CANDIDATE_V0_1.md) distingue exploration, qualification, puis production. L'[horizon de reconnaissance](../../documentation/architecture/HORIZON_RECONNAISSANCE_FORMATS.md) définit ainsi le client consommateur : « Télécharge et épingle les versions approuvées ; reconnaît, extrait, contrôle et journalise localement. »

L'exploitation visée est :

1. Récupérer les profils et capacités approuvés dans un cache local, avec versions et empreintes vérifiées.
2. Caractériser le document et rechercher une correspondance native ou structurelle lorsque nécessaire.
3. Choisir un profil et un moteur compatibles dans leur périmètre qualifié ; refuser explicitement les cas inconnus, ambigus ou incompatibles.
4. Exécuter le traitement requis, contrôler schéma et règles métier disponibles, puis restituer données, statuts, preuves, versions et limites.
5. Permettre au consommateur de gérer la revue, les erreurs et les mises à jour selon une politique explicite.

Cette cible n'est pas livrée. Le contrat de sortie commun reste à définir. Les documents restent locaux ; aucun appel à ChatGPT n'est nécessaire au fonctionnement nominal. Le client fournit le traitement ; la GED ou l'application consommatrice conserve le classement, le stockage et l'usage métier. Une escalade peut utiliser le [contrat existant](../escalade-consommateur/README.md), sans transmission automatique de données privées.

La [dette C du lecteur invoice2data](documentation/DETTE_INVOICE2DATA_LECTEUR.md) décrit le défaut bloquant et ses critères de clôture. La [feuille de route générale](../../documentation/FEUILLE_DE_ROUTE.md) ordonne les étapes du projet.

## Ce qu'il reste à développer ou qualifier

| Chantier | Acquis disponibles | Écart à combler |
| --- | --- | --- |
| Adaptateurs fiables | Commandes EML/OCR candidates, chargement invoice2data corrigé | Corriger C ; éprouver chaque interface et ses erreurs. |
| Frontières logicielles lisibles | Capacités et références du registre Builder | Arbitrer la place des outils de préparation et du code partagé ; éviter les implémentations redondantes. |
| Chaîne d'exploitation | Résolveur limité et adaptateurs appelables séparément | Définir l'entrée commune et relier caractérisation, sélection, exécution et contrôles. Éprouver les refus autant que les succès. |
| Catalogue local maîtrisé | Git, index, registres et empreintes | Synchronisation/cache, compatibilité, version épinglée et politique de mise à jour/retrait, vérifiés hors du dépôt de développement. |
| Reconnaissance et sélection | Résolution native et matchers ULISTAG candidats | Relier observations, TAGs et profils ; gérer ambiguïtés et qualification. Mesurer les faux positifs sur corpus indépendants. |
| Résultat commun | JSON et traces spécifiques, schémas existants | Définir une enveloppe et des statuts communs ; intégrer contrôles métier et preuves pertinentes. |
| Ressources qualifiées | Candidats, oracles, preuves et dettes | Phase 2 : variantes indépendantes, négatifs, exactitude, performances et décision bornée. GED-04 reste différé et GED-05 en pause. |
| Usage chez un consommateur | Primitives locales et contrat d'escalade candidat | Recette indépendante d'installation et de bout en bout, interface d'appel, journalisation, mises à jour et reprise sur erreur. Aucun connecteur GED général livré ici. |

La phase 3 nécessite à la fois une chaîne logicielle fiable et des profils qualifiés. Cette liste rend le travail restant visible ; elle n'autorise pas automatiquement sa réalisation ni la reprise des expériences suspendues. La correction C reste à valider séparément.

## Installation, exemples et vérification

Le [profil complet Ubuntu](../deploiement/ubuntu/complete-v0_1/README.md) décrit les dépendances et environnements isolés. Les manifestes décrivent deux capacités particulières : [invoice2data](deployment/invoice2data_manifest_v0_1.json) et [OCR par profil](deployment/profile_ocr_extract_manifest_v0_1.json). Ils ne décrivent pas un client unifié.

Pour un exemple d'extraction EML sur corpus public, voir [les résultats GED-03](../../experiences/administration-droits/GED-03/RESULTS_V0_1.md). Les commandes de [vérification du dépôt](../verification/VERIFIER_LE_DEPOT.md) contrôlent les vecteurs et contrats couverts ; elles ne valent pas qualification des moteurs ni recette terrain.

L'installation neuve d'invoice2data et les imports passent avec `invoice2data==0.4.5` et `setuptools==80.9.0`. Son extraction fonctionnelle reste en échec tant que C n'est pas corrigée. Le profil complet n'est donc pas déclaré stable sans réserve.
