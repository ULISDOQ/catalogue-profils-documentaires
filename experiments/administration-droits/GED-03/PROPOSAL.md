# GED-03 — Proposition phase 1 : courriel .EML structuré

Référence : GED03-PROPOSAL-001
Statut : proposition d'expérience ; aucune implémentation autorisée par ce document.

## Pourquoi ce cas

GED-01 et GED-02 ont principalement éprouvé des documents visuels/PDF. GED-03 doit tester l'inverse : un conteneur déjà structuré pour lequel GED-core doit supprimer les traitements inutiles.

Un .eml expose nativement en-têtes, adresses, date, sujet, corps multipart, pièces jointes, types MIME et Message-ID.

Chaîne candidate :
EML -> parseur MIME local -> objet message normalisé -> contrat de champs -> couche sémantique éventuelle.

Reconnaissance visuelle = NOT_REQUIRED.
OCR = NOT_REQUIRED pour le message.
ULISTAG spécialisé = NOT_REQUIRED sauf découverte contraire.

## Corpus synthétique proposé

Positifs :
- S01 texte simple ;
- S02 HTML + texte alternatif ;
- S03 pièce jointe PDF ;
- S04 plusieurs destinataires ;
- S05 en-têtes pliés / encodages RFC ;
- S06 nom de pièce jointe Unicode.

Négatifs/limites :
- N01 fichier texte renommé .eml ;
- N02 MIME malformé ;
- N03 message tronqué.

## Contrat minimal de sortie

message_id, date, from, to, cc, subject, body_text, body_html_present, attachments, mime_structure, parse_status.

Pas d'interprétation métier du contenu dans la première passe.

## Réemploi attendu

Réutiliser : méthode GED-N, contrats profil/version/preuve, registre, statuts, traçabilité SHA/version et principes de déploiement isolé.

Ne pas réutiliser artificiellement : OCR géométrique GED-02, visual-keypoints, anchor-graph, binding 2044. Ce non-réemploi est une preuve positive d'adaptation.

## Primitive à évaluer avant toute invention

Bibliothèque standard Python email. Une dépendance supplémentaire n'est justifiée que par une insuffisance observée.

## Critères de réussite

C1 caractérisation : identifier le conteneur structuré et l'inutilité de l'OCR.
C2 réemploi : réutiliser les contrats génériques sans recopier les spécificités 2044.
C3 extraction : produire les champs depuis MIME avec provenance.
C4 négatifs : ne pas accepter silencieusement les messages invalides.
C5 sobriété : OCR_CALLS=0 ; VISUAL_MATCHER_CALLS=0 ; LLM_CALLS=0 ; NETWORK_REQUIRED=0.
C6 industrialisation : mesurer composants réutilisés, configuration, primitive nouvelle, coût de fabrication, limites et capitalisation.

## Risques hors périmètre initial

Normalisation avancée des adresses, DKIM/SPF, identité réelle de l'expéditeur, analyse sémantique du contenu, exécution/ouverture des pièces jointes.

## Décision proposée

NEXT_GED=GED-03
DOCUMENT_FAMILY=COURRIEL_EML
PRIMARY_EXPERIMENT=GED_CORE_ADAPTIVE_PROFILE_FACTORY
IMPLEMENTATION=NOT_YET_AUTHORIZED