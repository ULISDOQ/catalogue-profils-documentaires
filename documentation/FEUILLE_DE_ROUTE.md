# Feuille de route ULISDOQ

Mise à jour : **29 octobre 2026 — clôture de séance**.  
Cette page ordonne la reprise et les étapes ultérieures. L'[état du projet](ETAT_DU_PROJET.md) décrit les acquis et limites ; Git conserve leurs versions. Une étape prévue n'est pas une autorisation générale de l'exécuter : Jean valide les périmètres au fur et à mesure.

## Point d'arrêt

- Organisation générale à quatre espaces et racine relues, acceptées : catalogue, logiciels, expériences, documentation.
- Correction A intégrée : lanceur du Builder 0.1.3, distribution reconstruite et plan inchangé.
- Correction B intégrée : dépendance de compatibilité invoice2data et manifestes alignés, installation neuve et imports vérifiés.
- Client documenté : commandes réelles, limites, superpositions, cible phase 3 et travaux manquants. Cela ne tranche pas les futures frontières logicielles.
- Dernière recette logicielle : **37 tests et selftest PASS** ; batterie complète **30/31**, extraction facture encore bloquée par C. Aucun profil n'est qualifié pour la production.
- GED-05 en pause ; dettes de qualification GED-02/GED-04 différées. Aucun déploiement consommateur n'a été exécuté pendant ce chantier.

## Reprise et étapes ordonnées

| Ordre | Étape | État / décision nécessaire | Résultat attendu pour passer à la suite |
| --- | --- | --- | --- |
| 1 | Corriger le lecteur invoice2data | [Dette C ouverte](../logiciels/client/documentation/DETTE_INVOICE2DATA_LECTEUR.md) ; correction à autoriser séparément | Appel API corrigé, tests de lecteur et extraction synthétique, manifeste et documentation alignés, commit vérifié. |
| 2 | Recevoir le socle logiciel après A/B/C | Après C ; limites d'environnement à conserver explicitement | Recette reproductible par composant et batterie complète sur les versions retenues ; identifier les réserves restantes. Une réussite locale ne remplace pas la recette sur un environnement consommateur. |
| 3 | Arbitrer les frontières logicielles | Discussion ouverte : client, outils de préparation, Builder et capacités partagées | Responsabilités et dépendances compréhensibles ; distinguer réemploi utile et duplication réelle avant tout rangement. Voir [les superpositions du client](../logiciels/client/README.md). |
| 4 | Relire et simplifier les documents internes | Racine traitée ; sous-dossiers encore à examiner par périmètres validés | Re-parsage critique, fusions utiles, retrait motivé de l'inutile avec reconstructibilité conservée ; roadmaps des composants actualisées. |
| 5 | Aligner POM, architecture et dépôt | Après les décisions retenues aux étapes précédentes | [POM](MODELE_OPERATOIRE_PROJET.md), interfaces, manifestes et organisation concordants ; distinguer cible, implémentation et qualification. |
| 6 | Poursuivre la phase 1 documentaire et les outils utiles | Selon priorités validées ; GED-05 ne reprend pas automatiquement | Nouveaux cas autorisés, connaissances réutilisables, preuves et dettes explicites ; progrès du Builder et du client proportionnés aux besoins observés. |
| 7 | Qualifier profils et capacités en phase 2 | Chantier ultérieur à ouvrir explicitement | Variantes et négatifs indépendants, exactitude sémantique, robustesse, performances, décisions bornées de qualification ; reprise des dettes documentées. |
| 8 | Éprouver puis livrer l'exploitation de phase 3 | Conditionnée par logiciel fiable et ressources qualifiées | Installation et recette indépendantes, traitement local de bout en bout, interfaces documentées, mises à jour et erreurs maîtrisées. |

L'ordre n'empêche pas un arbitrage motivé si une dépendance apparaît ; il évite de relancer tous les chantiers à la reprise. La prochaine discussion porte sur C, sans la considérer déjà autorisée ou corrigée.

## Où retrouver le détail

- [Dette C](../logiciels/client/documentation/DETTE_INVOICE2DATA_LECTEUR.md) : défaut, proposition et critères de clôture.
- [Client](../logiciels/client/README.md) : capacités présentes et écarts avant une chaîne d'exploitation complète.
- [Logiciels](../logiciels/README.md) : responsabilités et limites de chaque ensemble.
- [Roadmap Builder](../logiciels/profile-builder/ROADMAP.md) et [roadmap ULISTAG](../logiciels/ULISTAG/ROADMAP.md) : chantiers spécialisés, à relire avec leurs états d'implémentation actuels ; ce ne sont pas deux roadmaps générales concurrentes.
- [Journal des décisions](JOURNAL_DECISIONS.md), [organisation](architecture/ORGANISATION_DU_DEPOT.md) et [vérification](../logiciels/verification/VERIFIER_LE_DEPOT.md).

Travail dans `main`. Toute nouvelle branche exige une décision préalable de Jean. Aucun document source privé ou résultat personnel n'est publié ; les épreuves publiques utilisent des spécimens autorisés. Les dettes différées restent visibles et ne bloquent pas tous les travaux courants.

## Horizon

ULISDOQ vise un catalogue communautaire de connaissances documentaires réutilisables, d'abord francophone. L'hypothèse d'environ **10 000 profils documentaires** exprime une échelle crédible d'usages en production apportant des gains tangibles de reconnaissance, de classement et d'extraction. Ce n'est ni le volume déjà acquis ni une couverture ou un gain mesuré.

À l'horizon phase 3, un consommateur doit pouvoir récupérer et épingler les versions approuvées, reconnaître les documents dans le périmètre qualifié, appliquer les profils avec les briques compatibles, contrôler les résultats et en conserver la traçabilité localement. Inconnus, ambiguïtés et erreurs doivent rester explicites. Aucun appel à ChatGPT n'est requis au fonctionnement nominal ; les documents privés restent dans leur environnement autorisé.

Le Builder facilite la fabrication de candidats ; ULISTAG fournit la reconnaissance lorsqu'elle est nécessaire ; le client sert l'exploitation. Le catalogue reste l'actif principal. Voir le [prologue fondateur](../PROLOGUE_FONDATEUR.md) pour l'intention et l'adhésion au projet.
