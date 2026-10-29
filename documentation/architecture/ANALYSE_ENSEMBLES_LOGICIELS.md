# Cinq ensembles logiciels : acquis, frontières et promesse ULISDOQ

Analyse du 29 octobre 2026, fondée sur le code après correction C : `33e4316e851011333b04b44ed409b17cdef9250f`. Statut : **critique et proposition architecturale à discuter**, sans autorisation de déplacement, fusion ou développement des chantiers recensés.

## Conclusion

Les cinq ensembles examinés sont le client, Profile Builder, ULISTAG, l'escalade consommateur et le déploiement. La vérification est transverse ; le catalogue est l'actif documentaire principal, pas un sixième produit logiciel.

Ils ne forment pas cinq applications de même niveau : le client et le Builder portent deux usages, ULISTAG apporte des capacités partagées, l'escalade organise l'instruction d'un manque, le déploiement prépare les environnements. Leur présence dans cinq dossiers ne prouve pas qu'ils constituent déjà une chaîne opérationnelle.

**L'écart principal est l'assemblage contractuel et éprouvé entre catalogue, sélection, moteurs, contrôles et restitution.** La prochaine décision utile porte sur ces frontières et interfaces, avant un nouveau rangement ou la construction d'une plateforme supplémentaire.

## Trois entrées de lecture et de travail

| Entrée | Besoin | Acquis accessibles | Ce qui manque pour tenir la promesse |
| --- | --- | --- | --- |
| Consommateur | « J'ai un document et un besoin ; quelles données puis-je obtenir avec des ressources approuvées ? » | [Commandes du client](../../logiciels/client/README.md), adaptateurs, résolution native limitée et procédures de déploiement | Une entrée commune et un contrat de résultat ; sélection et refus maîtrisés ; catalogue local épinglé ; chaîne de bout en bout et recette indépendante. Le consommateur ne doit pas connaître les numéros GED. |
| Architecte | « Où sont les responsabilités, contrats, dépendances et niveaux de preuve ? » | [POM](../MODELE_OPERATOIRE_PROJET.md), [organisation](ORGANISATION_DU_DEPOT.md), horizons et manifestes | Relier chaque promesse à son contrat, implémentation et preuve ; actualiser les documents candidats ; distinguer profils et moteurs, décision et exécution, tests et qualification. Cette analyse ne remplace pas cette validation. |
| Développeur de brique | « Comment ajouter ou améliorer un moteur sans réécrire tous les consommateurs ? » | Adaptateurs Python, registre des capacités du Builder, manifestes et tests propres | Un contrat d'adaptateur commun : entrées, sorties, erreurs, prérequis, version, effets et compatibilités. Ajouter une brique au registre doit avoir une conséquence testée sur le parcours qui l'utilise. |

Un profil décrit le traitement et ses compatibilités ; un adaptateur appelle une brique. Un même adaptateur peut servir plusieurs profils. Un profil qualifié ne devient pas exécutable par tous les moteurs du seul fait de sa qualification.

## Critique des cinq ensembles

| Ensemble | Fonction à conserver | Implémentation constatée | Fragilité / développement nécessaire |
| --- | --- | --- | --- |
| **Client** | Exploiter localement les ressources documentaires | Commandes distinctes : facture, EML, OCR piloté par profil, résolution et édition de TAG. Facture corrigée par C. | Il mélange exploitation et préparation. Pas d'entrée ni de résultat communs ; le TAG OCR est encore fourni manuellement. Définir une chaîne de sélection/exécution/contrôle ; arbitrer la place de l'éditeur de TAG et des adaptateurs partagés. |
| **Profile Builder** | Aider à fabriquer et éprouver des profils candidats | CLI `info`, `plan`, `selftest` ; planner déterministe natif/matchers, registre de capacités | Pas de matérialisation automatique ni d'exécution. Le registre est plus large que les compositions réellement prises en charge par le planner. Le statut `PROFILE_CANDIDATE_PRODUCED` peut donner l'impression d'un profil créé alors que la sortie reste un plan. Clarifier le contrat avant d'ajouter build/test/package. |
| **ULISTAG** | Observer et reconnaître les structures quand le format natif ne suffit pas | Matchers candidats ancres et points visuels, références, schémas et protocoles | Pas de recherche globale qualifiée sur le catalogue. Définir observation et résultat communs, pré-sélection/index, liaison TAG–profils et arbitrage des ambiguïtés. Qualifier faux positifs et variantes avant la production ; un hash stable n'est pas une preuve d'identité documentaire. |
| **Escalade consommateur** | Transformer un manque en demande examinable et en retour documentaire versionné | Validation locale de champs, accusé/ledger et contrôle de cohérence d'un cycle | Le CLI n'instruit pas lui-même le besoin, ne transporte pas automatiquement les échanges et n'applique pas le profil produit. Les champs de confidentialité sont des déclarations contrôlées, pas une anonymisation du contenu libre. Prévoir instruction/revue et preuve de reprise ; ne pas l'imposer à chaque document courant. |
| **Déploiement** | Installer ou rattacher les dépendances puis vérifier une combinaison explicite | Profil Ubuntu complet, environnements isolés, propriété, rattachement, batterie et rollback protégé | L'installation neuve est distincte de la mise à niveau. Un environnement possédé existant est réutilisé avant réinstallation des requirements : une évolution comme B ne s'y applique pas automatiquement. La batterie peut détecter un écart mais ne le corrige pas. Concevoir une migration contrôlée et éprouver installation/mise à jour/rollback chez un consommateur. |

### Sources et limites des constats

- Client : [adaptateur facture](../../logiciels/client/extract.py), [résolveur](../../logiciels/client/profile_resolver_v0_1.py), [OCR](../../logiciels/client/profile_ocr_extract_v0_1.py). Le résolveur ne lit que le mode natif, MIME et extension ; il retourne MATCH pour le candidat EML sans imposer sa qualification.
- Catalogue : [index canonique](../../catalogue/index.json) et [registre de profils](../../catalogue/registre-profils.json). Ce sont deux vues de périmètres différents, pas des doublons à fusionner arbitrairement. Leur articulation pour un consommateur reste à contractualiser : le registre référence des candidats expérimentaux ; leur présence ne les promeut pas.
- Builder : [CLI](../../logiciels/profile-builder/ulisdoq_profile_builder/cli.py), [planner](../../logiciels/profile-builder/ulisdoq_profile_builder/planner.py) et [registre des capacités](../../logiciels/profile-builder/registry/CAPABILITY_REGISTRY_V0_1.json). Les branches de sélection présentes concernent le parsing natif et les classes de matchers ; une capacité simplement déclarée n'est pas une chaîne générique déjà exécutée.
- ULISTAG : [roadmap](../../logiciels/ULISTAG/ROADMAP.md) et [protocole de TAG candidat](../../logiciels/client/documentation/PROTOCOLE_TAG_CANDIDAT.md). L'index local et les critères de reconnaissance restent des travaux à conduire et qualifier.
- Escalade : [CLI](../../logiciels/escalade-consommateur/bin/ulisdoq-escalation). `validate_request` contrôle notamment des indicateurs de confidentialité ; cela ne démontre pas que le texte libre est expurgé. Le contrôle de cycle vérifie une cohérence de références déclarées, pas à lui seul l'existence du contenu à chaque commit distant.
- Déploiement : [ensure_env et commandes](../../logiciels/deploiement/ubuntu/complete-v0_1/ulisdoq-deploy.sh), [batterie](../../logiciels/deploiement/ubuntu/complete-v0_1/verify_complete.py) et [compatibilité](../../logiciels/deploiement/ubuntu/complete-v0_1/COMPATIBILITY.md). Les références personnelles ou à un projet extérieur encore présentes dans certains documents internes sont une dette de relecture, pas un prérequis de l'architecture communautaire.

## Assemblage proposé, sans nouveau rangement

| Parcours | Enchaînement visé | Frontière à préserver |
| --- | --- | --- |
| Exploiter | Document et besoin → ressources locales épinglées → sélection compatible → adaptateurs → contrôles → résultat au consommateur | Aucun profil candidat automatiquement promu ; aucune donnée privée publiée. ULISTAG seulement lorsque nécessaire. |
| Fabriquer | Besoin nouveau et corpus autorisé → Builder → essais avec les capacités partagées → paquet candidat → revue/qualification → catalogue | Le Builder ne décide pas seul de la qualification ou de la publication ; pas de seconde implémentation des extracteurs. |
| Résoudre un manque | Refus documenté → éventuelle demande minimisée → instruction/revue → ressource versionnée → nouvelle épreuve locale | L'escalade reste explicite et séparée du traitement courant ; elle n'est pas un appel automatique à une IA ni un export du document. |

Déploiement et vérification soutiennent ces parcours. Les deux premiers doivent réemployer un socle de capacités commun ; décider s'il faut une bibliothèque identifiée ou seulement des interfaces partagées demande un inventaire de dépendances et un arbitrage. Aucun nouveau dossier racine n'est nécessaire pour poser ce contrat.

## Priorités proposées à arbitrer

1. **Rendre l'usage actuel consommable** : une épreuve locale documentée sur une famille existante, avec version épinglée, sélection explicable, résultat et refus. Le candidat reste marqué candidat ; ne pas inventer une qualification de production pour la démonstration.
2. **Établir les interfaces communes** : observation, choix de profil, invocation d'une brique, résultat et erreur ; une table minimale de compatibilité profil–adaptateur–moteur. Choisir les frontières du socle partagé et la place de l'édition de TAG avant les déplacements.
3. **Rendre le catalogue distribuable pour cet usage** : articulation des deux vues, statuts, empreintes, cache et politique de mise à jour/retrait. Puis traiter la migration des environnements existants ; une installation neuve réussie ne clôt pas ce chantier.
4. **Compléter la fabrique sur ces mêmes contrats** : essais et paquet candidat, en corrigeant l'ambiguïté entre plan produit et profil matérialisé. Ne pas créer un deuxième runtime de traitement documentaire dans le Builder.
5. **Qualifier par périmètre** : variantes, négatifs, sémantique, performances et recette consommateur. C'est la phase 2 à ouvrir explicitement ; GED-04 reste différé et GED-05 en pause.

Ces priorités sont des propositions, pas une extension de l'autorisation de corriger C. Les promesses de phase 3 ne sont pas réalisées par la seule remise en ordre des dossiers.

## Recette après C

Au commit `33e4316e851011333b04b44ed409b17cdef9250f`, checkout propre : **44 tests du dépôt et selftest PASS ; 3 tests d'intégration invoice2data PASS ; 31/31 contrôles de la batterie complète PASS**. Facture et modèle entièrement synthétiques ; lecteurs text/pdftotext, champs attendus comparés. L'adaptateur est en 0.1.1-phase1 et son manifeste vérifie le nouveau blob. La [dette C](../../logiciels/client/documentation/DETTE_INVOICE2DATA_LECTEUR.md) conserve le diagnostic et la recette.

Environnement : Ubuntu 24.04.3, Python 3.12.14, Tesseract 5.3.4 ; données françaises chargées depuis un répertoire de diagnostic isolé. Les environnements core, ancres et extraction ont été recréés pour la recette après constat de lanceurs devenus indisponibles dans les anciennes copies temporaires. Aucun installateur système ni déploiement consommateur exécuté.

La batterie contrôle des capacités bornées ; elle ne prouve pas la chaîne automatique client–catalogue, la qualification des profils, tous les lecteurs ou l'installation/mise à jour/rollback. Le vérificateur visuel historique exige toujours Python exact 3.12.3 : cette réserve distincte n'est pas effacée par le PASS de la batterie globale. Le déploiement complet conserve son statut candidat.

L'[horizon architectural](HORIZON_RECONNAISSANCE_FORMATS.md) et la [feuille de route générale](../FEUILLE_DE_ROUTE.md) restent les références pour la cible et l'ordre des arbitrages.
