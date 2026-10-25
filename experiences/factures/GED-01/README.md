# GED-01 — Une facture, un profil, un résultat

Cette expérience appartient à la famille [Factures & achats](../README.md).

**Objectif pour les relecteurs :** montrer comment un document d'expérience peut être reconnu et exploité avec un profil partageable, sans envoyer de données à ULISDOQ.

## Commencer ici (5 minutes)

1. **Voir le document source expérimental :** [facture Fournisseur-EXP-01 modifiée (PDF image)](specimens/Fournisseur-EXP-01_document_experimental.pdf), ou [page 1](specimens/Fournisseur-EXP-01_page_1.png) et [page 2](specimens/Fournisseur-EXP-01_page_2.png).
2. **Voir le profil candidat :** [fournisseur_exp_01.yml](modeles/fournisseur_exp_01.yml), au format d'[invoice2data](https://github.com/invoice-x/invoice2data).
3. **Voir le client ULISDOQ :** [mode d'emploi et commande](../../../client/README.md) ; [script Python](../../../client/extract.py).
4. **Voir comment juger le résultat :** [protocole](documentation/PROTOCOLE.md).

**État actuel :** le candidat ULISTAG v0.1 a passé une première exécution réelle sur un environnement Linux indépendant : `MATCH_CANDIDATE`, `node_ratio=1.0`, `edge_ratio=1.0`, puis extraction technique des trois champs attendus avec `EXTRACTED_UNVERIFIED`. Aucune valeur privée n'a été retournée. Ce résultat porte sur la source ayant servi à la conception et reste **non qualifié**. Voir le [RETEX environnement indépendant](documentation/RETEX_ULISTAG_V0_1_INDEPENDENT_ENV_EXECUTION_001.md).

Voir la [conception spécialisée GED-01](ulistag/ANCHOR_GRAPH_V0_1.md). Le matcher générique candidat correspondant vit désormais dans le cœur [ULISTAG/](../../../ULISTAG/README.md).

Pour préparer un descripteur local, voir [l'éditeur de TAG candidat](../../../client/tag_candidate.py) et son [protocole](../../../project/TAG_CANDIDATE_PROTOCOL.md). La consultation du catalogue reste à implémenter.

## Séparation des identités

Le nom **Fournisseur-EXP-01** est un alias limité à cette expérience. Le profil technique utilise une référence opaque, sans prétendre identifier l'émetteur. L'architecture cible sépare [entité canonique, TAG de format, profil et correspondances](../../../project/HORIZON_IDENTITY_MAPPING.md). La reconnaissance du format doit être qualifiée indépendamment de l'identité commerciale.

## Ce que doit apporter ULISDOQ

ULISDOQ publie un **profil versionné et vérifiable**, ainsi que des fixtures et des contrôles. Il **ne reçoit pas les factures de production**. Un outil tiers (GED, script ou application métier) récupère une version précise du catalogue et exécute localement un moteur tel qu'invoice2data, puis vérifie le résultat.

```text
Document local → profil ULISDOQ versionné → OCR + invoice2data
               → JSON d'extraction → contrôles du client → GED du client
```

L'adaptateur utilise invoice2data ; la réussite d'extraction reste à démontrer.

## Pourquoi ces données ?

Le PDF et les deux PNG sont des **dérivés d'une facture Fournisseur-EXP-01 réelle avec données modifiées**, signalés comme documents expérimentaux sans valeur contractuelle. Ils ne doivent pas être confondus avec une facture originale, ni avec une certification de leur anonymisation. Les droits sur la présentation commerciale peuvent subsister ; ce cas ne vaut pas autorisation générale de reproduire des factures tierces.

Pour contribuer : proposer une amélioration du profil, une exécution reproductible ou une critique précise ; ne pas déposer de facture personnelle brute.

## Réutilisation opérationnelle cible

Une fois un profil **qualifié**, un consommateur (GED, script ou autre) récupère via l'API GitHub une **version immuable** du profil ULISDOQ, vérifie son identité et sa compatibilité, puis la conserve en cache local. Chaque facture Fournisseur-EXP-01 suivante est traitée localement avec ce profil, un moteur OCR et invoice2data ; les contrôles métier vérifient les résultats avant admission dans la GED.

- **Réseau :** accès GitHub seulement pour obtenir ou mettre à jour les profils ; aucune facture transmise au catalogue.
- **Autonomie :** pas d'appel à ChatGPT ni à un LLM requis pour le fonctionnement nominal ; le cache permet de poursuivre hors ligne.
- **Sécurité :** ne pas charger automatiquement une nouvelle version non qualifiée ; figer le commit ou l'empreinte approuvée.
- **Évolution :** si signature de facture inconnue, extraction ambiguë ou contrôles en échec, renvoyer un état explicite et ouvrir un travail de qualification ; ne pas inventer de valeurs.

**État actuel : architecture cible documentée, pas encore réalisée de bout en bout.** Le client ULISDOQ présent dans `client/extract.py` ne télécharge pas encore les profils depuis l'API GitHub et le profil Fournisseur-EXP-01 n'est pas qualifié.
