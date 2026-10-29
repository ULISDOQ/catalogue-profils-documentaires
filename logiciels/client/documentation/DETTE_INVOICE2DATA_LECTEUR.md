# Dette C — lecteur de l'adaptateur invoice2data

Identifiant : **DETTE-CLIENT-INVOICE2DATA-LECTEUR-001**  
Statut : **OUVERTE — CORRECTION NON INTÉGRÉE**  
Constat et mise en attente : 29 octobre 2026.  
Périmètre : [adaptateur facture](../extract.py), pas le profil GED-01 ni le catalogue.

## Défaut et effet

L'adaptateur transmet `args.reader`, une chaîne telle que `pdftotext` ou `tesseract`, à l'argument `input_module` de `invoice2data.extract_data`. L'API installée en version 0.4.5 attend un module possédant une fonction `to_text`.

Après correction de la dépendance B, l'import fonctionne mais l'extraction échoue : `AttributeError: 'str' object has no attribute 'to_text'`. L'adaptateur retourne `ERROR`. Le défaut existait avant la réorganisation du dépôt.

Reproduction générique, avec une facture et un modèle YAML compatibles, dans l'environnement invoice2data déclaré :

```text
python extract.py DOCUMENT --templates REPERTOIRE_MODELES --reader pdftotext
```

Ce n'est pas une commande directement exécutable sans fournir ces ressources et leurs chemins. La recette utilise une fixture entièrement synthétique ; aucun document privé n'est requis.

## Correction envisagée

Résoudre le lecteur demandé vers le module correspondant sous `invoice2data.input`, puis transmettre ce module à `extract_data`. Conserver une erreur explicite si le lecteur est inconnu, indisponible ou échoue. Vérifier les lecteurs acceptés et leurs prérequis au lieu de présumer leur compatibilité.

Un prototype de diagnostic hors dépôt a déjà extrait la facture synthétique attendue : identifiant `TEST-001`, montant `42.0`, devise `EUR`, date `2026-01-01`, statut `EXTRACTED_UNVERIFIED`. Ce résultat ne signifie pas que le code courant est corrigé ou qu'un profil est qualifié.

## Conditions de clôture

1. Autorisation du lot de correction C, puis modification ciblée de l'adaptateur.
2. Tests du vrai appel : lecteur valide, lecteur inconnu et extraction synthétique avec comparaison des champs attendus ; erreur lisible et code retour cohérent en cas d'échec.
3. Actualisation de l'empreinte de l'implémentation dans le [manifeste client](../deployment/invoice2data_manifest_v0_1.json) et des mentions de dette dans la documentation courante.
4. Tests du dépôt et batterie complète rejoués dans les environnements déclarés ; consigner le commit, les versions et les résultats. Ne pas affaiblir les contrôles pour obtenir PASS.
5. Vérification du commit intégré dans `main`, puis mise à jour explicite du statut de cette dette. Pas de qualification de production déduite de cette seule correction.

## Référence de reprise

État logiciel inchangé depuis `af748a72545d02fe3eba5d7df6d2b852c7941e5e` : A et B corrigées ; 37 tests et selftest PASS. Batterie complète observée : **30/31 PASS**, seul `functional_invoice_extraction` en échec, avec données OCR françaises de diagnostic isolées. La réserve du vérificateur visuel historique sur Python exact 3.12.3 est distincte et reste conservée.

L'[état du projet](../../../documentation/ETAT_DU_PROJET.md) donne les autres limites. La [feuille de route générale](../../../documentation/FEUILLE_DE_ROUTE.md) situe cette dette dans l'ordre de reprise. Aucun déploiement consommateur, reprise GED-05 ou qualification phase 2 n'est autorisé par cette fiche.
