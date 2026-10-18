# GED-01 — Une facture, un profil, un résultat

**Objectif pour les relecteurs :** montrer comment un document d'expérience peut être reconnu et exploité avec un profil partageable, sans envoyer de données à ULISDOQ.

## Commencer ici (5 minutes)

1. **Voir le document source expérimental :** [facture Fournisseur-EXP-01 modifiée (PDF image)](fixtures/Fournisseur-EXP-01_document_experimental.pdf), ou [page 1](fixtures/Fournisseur-EXP-01_page_1.png) et [page 2](fixtures/Fournisseur-EXP-01_page_2.png).
2. **Voir le profil candidat :** [fournisseur_exp_01.yml](templates/fournisseur_exp_01.yml), au format d'[invoice2data](https://github.com/invoice-x/invoice2data).
3. **Voir le client :** [mode d'emploi et commande](client/README.md) ; [script Python](client/extract.py).
4. **Voir comment juger le résultat :** [protocole](docs/PROTOCOLE.md).

**État réel :** le document et le code sont publiés ; le client et le profil n'ont **pas encore été exécutés ensemble ni qualifiés** sur ce PDF. Aucun taux de réussite n'est revendiqué.

## Ce que doit apporter ULISDOQ

ULISDOQ publie un **profil versionné et vérifiable**, ainsi que des fixtures et des contrôles. Il **ne reçoit pas les factures de production**. Un outil tiers (GED, script ou application métier) récupère une version précise du catalogue et exécute localement un moteur tel qu'invoice2data, puis vérifie le résultat.

```text
Document local → profil ULISDOQ versionné → OCR + invoice2data
               → JSON d'extraction → contrôles du client → GED du client
```

Le lien avec invoice2data est désormais **concret dans le code**, mais la réussite d'extraction reste à prouver. Les SVG de reconstitution ont été retirés pour éviter un deuxième jeu documentaire.

## Pourquoi ces données ?

Le PDF et les deux PNG sont des **dérivés d'une facture Fournisseur-EXP-01 réelle avec données modifiées**, signalés comme documents expérimentaux sans valeur contractuelle. Ils ne doivent pas être confondus avec une facture originale, ni avec une certification de leur anonymisation. Les droits sur la présentation commerciale peuvent subsister ; ce cas ne vaut pas autorisation générale de reproduire des factures tierces.

## Compléments secondaires

Le premier exemple entièrement fictif en texte brut (`facture_fictive_001.txt`, `attendu_001.json`, `profil_facture_fictive_001.json` et `cas_ged01.json`) reste disponible comme matériau préparatoire ; **il ne fait pas partie du chemin de preuve Fournisseur-EXP-01**.

Pour contribuer : proposer une amélioration du profil, une exécution reproductible ou une critique précise ; ne pas déposer de facture personnelle brute.

## Réutilisation opérationnelle cible (sans ChatGPT)

Une fois un profil **qualifié**, un consommateur (GED, script ou autre) récupère via l'API GitHub une **version immuable** du profil ULISDOQ, vérifie son identité et sa compatibilité, puis la conserve en cache local. Chaque facture Fournisseur-EXP-01 suivante est traitée localement avec ce profil, un moteur OCR et invoice2data ; les contrôles métier vérifient les résultats avant admission dans la GED.

- **Réseau :** accès GitHub seulement pour obtenir ou mettre à jour les profils ; aucune facture transmise au catalogue.
- **Autonomie :** pas d'appel à ChatGPT ni à un LLM requis pour le fonctionnement nominal ; le cache permet de poursuivre hors ligne.
- **Sécurité :** ne pas charger automatiquement une nouvelle version non qualifiée ; figer le commit ou l'empreinte approuvée.
- **Évolution :** si signature de facture inconnue, extraction ambiguë ou contrôles en échec, renvoyer un état explicite et ouvrir un travail de qualification ; ne pas inventer de valeurs.

**État actuel : architecture cible documentée, pas encore réalisée de bout en bout.** Le client local présent dans `client/extract.py` ne télécharge pas encore les profils depuis l'API GitHub et le profil Fournisseur-EXP-01 n'est pas qualifié.
