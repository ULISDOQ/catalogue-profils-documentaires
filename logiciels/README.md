# Logiciels ULISDOQ

Les logiciels servent le catalogue documentaire. Une brique technique exécute une opération ; un profil décrit le traitement et ses compatibilités. Le consommateur exploite ces ressources, tandis que la fabrication d'un profil reste un autre usage.

| Ensemble | Rôle | État actuel |
| --- | --- | --- |
| [Client](client/README.md) | Exploiter localement des profils existants et restituer les résultats | Plusieurs commandes candidates, pas un client unifié : facture, EML, OCR, résolution et outil de préparation de TAG. Le README expose les sorties, les superpositions actuelles, l'horizon phase 3 et les travaux restants. |
| [Profile Builder](profile-builder/README.md) | Aider à fabriquer un profil candidat | 0.1.3 : sélection de capacités et planification, sans exécution des moteurs ni matérialisation de profil. |
| [ULISTAG](ULISTAG/README.md) | Reconnaître une structure documentaire lorsque nécessaire | Matchers, protocoles et preuves candidats ; reconnaissance distincte de l'extraction et de la qualification. |
| [Escalade consommateur](escalade-consommateur/README.md) | Instruire un manque rencontré par un consommateur | Contrat Git et cycle candidats ; pas de transfert automatique de documents privés. |
| [Déploiement](deploiement/ubuntu/complete-v0_1/README.md) | Préparer et vérifier les environnements | Profil Ubuntu candidat ; chargement invoice2data corrigé, extraction encore bloquée par C. |
| [Vérification](verification/VERIFIER_LE_DEPOT.md) | Contrôler cohérence et régressions couvertes | Contrats, empreintes, liens et vecteurs ; couverture distincte de la qualification des moteurs et du terrain. |

Client et Builder doivent réemployer les mêmes adaptateurs et moteurs. Leur code ne doit pas être dupliqué. Le rangement actuel mélange encore préparation et exploitation ; les choix de séparation ou de fusion restent à arbitrer, sans déplacement décidé par cette description.

Les cas et preuves restent dans les expériences ; les connaissances réutilisables appartiennent au catalogue. L'[état du projet](../documentation/ETAT_DU_PROJET.md) conserve les limites et décisions courantes.
