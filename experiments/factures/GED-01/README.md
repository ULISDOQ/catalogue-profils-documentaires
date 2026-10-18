# GED-01 — Facture expérimentale Fournisseur-EXP-01

Cette expérience appartient à la famille [Factures](../README.md). Elle éprouve un modèle de facture particulier ; elle ne définit pas à elle seule le fonctionnement général des profils de factures ULISDOQ.

## Périmètre

La fixture publiée est dérivée d'une facture réelle avec données modifiées. L'original reste privé et local. Le profil candidat `fournisseur_exp_01.yml` a été construit pour ce modèle et doit être éprouvé sur la source originale puis sur des positifs indépendants et des contre-exemples avant toute généralisation.

## Commencer ici

1. [Fixture PDF expérimentale](fixtures/Fournisseur-EXP-01_document_experimental.pdf), [page 1](fixtures/Fournisseur-EXP-01_page_1.png), [page 2](fixtures/Fournisseur-EXP-01_page_2.png).
2. [Profil invoice2data candidat](templates/fournisseur_exp_01.yml).
3. [Client ULISDOQ](../../../client/README.md) et [script d'extraction](../../../client/extract.py).
4. [Protocole GED-01](docs/PROTOCOLE.md).

Pour préparer un descripteur local, voir [l'éditeur de TAG candidat](../../../client/tag_candidate.py) et le [protocole TAG](../../../project/TAG_CANDIDATE_PROTOCOL.md).

## État

Le cas est **expérimental et non qualifié**. Le rapprochement structurel, l'attribution du profil, l'extraction sur la source originale et la qualification restent des étapes distinctes.

Le nom **Fournisseur-EXP-01** est un alias d'expérience. L'architecture canonique distingue [entité, format/TAG et profil](../../../project/HORIZON_IDENTITY_MAPPING.md).

## Confidentialité

Aucune facture originale privée ne doit être publiée dans le dépôt. Les fixtures publiées doivent rester explicitement identifiées comme expérimentales et faire l'objet d'une revue de confidentialité et de droits.
