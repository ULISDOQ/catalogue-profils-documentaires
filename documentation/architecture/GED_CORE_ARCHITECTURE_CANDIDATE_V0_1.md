# GED-core — Architecture candidate de fabrique générique de profils v0.1

Référence : GED-CORE-ARCH-001
Statut : architecture candidate ; aucune implémentation autorisée par cet objet.

## Formule

GED-core + Nouveau_document_N -> GED-N

GED-core n'est pas un moteur unique. Il organise la fabrication d'un profil candidat en recherchant d'abord le réemploi, puis la composition, puis seulement la spécialisation nécessaire.

## Acquis réutilisables déjà présents

- documentation/METHODE_GED_PHASE_1.md : cycle expérimental répétable.
- catalogue/registre-profils.json : découverte de profils.
- logiciels/client/tag_candidate.py : TAG candidat local.
- logiciels/ULISTAG/matchers/anchor_graph/ : reconnaissance structurelle texte.
- logiciels/ULISTAG/matchers/visual_keypoints/ : reconnaissance visuelle.
- logiciels/client/extract.py : extraction via moteur/template externe.
- logiciels/client/profile_ocr_extract_v0_1.py : extraction OCR géométrique pilotée par profil.
- schémas, manifests, preuves GED-01/GED-02 et profil de déploiement Ubuntu.

Ces éléments sont des capacités disponibles ; ils ne constituent pas encore une fabrique automatique.

## Chaîne minimale GED-core

INPUT nouveau document + besoin
-> CHARACTERIZE conteneur, structure native, texte, image, pages, contraintes
-> SEARCH_REUSE profil, matcher, lecteur, extracteur, grammaire existants
-> PLAN NO_EXTRA_PROCESSING | REUSE_PROFILE | ADAPT_PROFILE | COMPOSE | SPECIALIZE | UNSUPPORTED
-> BUILD_CANDIDATE profil + bindings + références + contrats + tests
-> ASSESS coût + qualité + robustesse + réutilisabilité + dettes
-> CAPITALIZE GED-N + promotion éventuelle vers GED-core/ULISTAG/grammaire

## Objets minimaux

1. Characterization : description factuelle avant choix du traitement.
2. Capability candidate : capacité existante, version, coût, dépendances, limites, preuves.
3. Processing plan : plan proportionné, y compris NO_EXTRA_PROCESSING.
4. Candidate profile package : identité/version, reconnaissance éventuelle, extraction éventuelle, contrat de champs, sémantique, sources, tests, preuves, maturité, limites, dette.

## GED-core vs ULISTAG-core

GED-core répond à : comment fabriquer le profil adapté ?
ULISTAG-core répond à : comment reconnaître structurellement le document quand cette reconnaissance est nécessaire ?

GED-core peut appeler ULISTAG-core, utiliser un parseur natif, utiliser OCR, utiliser un moteur spécialisé ou conclure qu'aucun traitement supplémentaire n'est nécessaire.

## Principe de décision

REUSE_BEFORE_SPECIALIZE
SPECIALIZE_BEFORE_INVENT
GENERALIZE_FROM_EVIDENCE

## Grammaires métiers

Le profil décrit où/comment obtenir une information. La grammaire métier décrit sa signification, ses relations et ses règles. Les règles métier réutilisables ne doivent pas être dupliquées dans chaque profil.

## Mesures phase 1

Pour chaque GED-N : composants réutilisés, configuration nouvelle, composants spécialisés, étapes humaines, étapes runtime, dépendances, coût de fabrication, qualité observée, échecs, actifs réutilisables et dettes.

## Non démontré à ce stade

- pas d'orchestrateur automatique GED-core ;
- pas de sélection automatique de capacités ;
- pas de génération autonome de profils ;
- pas de qualification automatique ;
- pas de registre universel de briques.

GED-N+1 doit d'abord vérifier que cette méthode de fabrication réduit réellement le coût du cas suivant avant toute plateforme.