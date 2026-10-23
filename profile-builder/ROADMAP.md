# Profile Builder — Roadmap de production

**Statut : chantier actif**

## M0 — contrat machine

Objectif : rendre les entrées et sorties minimales de GED-core Machine lisibles par une machine.

Livrables :

- GED_CORE_MACHINE_CONTRACT_V0_1 ;
- schéma CHARACTERIZATION ;
- schéma REQUESTED_NEED ;
- schéma CAPABILITY_REGISTRY ;
- schéma PROCESSING_PLAN ;
- schéma CANDIDATE_PROFILE_PACKAGE.

Gate M0 : les exemples GED-03 doivent pouvoir être décrits sans prose implicite.

## M1 — capability registry initial

Capitaliser les capacités déjà réellement présentes :

- parsing natif EML ;
- profile resolver CONTAINER_NATIVE ;
- ULISTAG anchor_graph ;
- ULISTAG visual_keypoints ;
- invoice2data adapter ;
- profile-driven OCR geometric extraction ;
- validation JSON Schema.

Gate M1 : aucune capacité déclarée sans version, interface, préconditions et limites.

## M2 — deterministic planner v0.1

Implémenter un moteur pur :

```text
characterization + requested_need + capability_registry + rules
→ processing_plan
```

Gate M2 : mêmes entrées sérialisées canoniquement = même plan et même hash.

## M3 — replay GED-03

Faire produire automatiquement le plan déjà observé pour GED-03.

Gate M3 : sélection du parseur MIME natif et exclusion déterministe OCR/vision/LLM.

## M4 — Profile Builder CLI minimal

Commandes candidates :

```text
profile-builder characterize
profile-builder plan
profile-builder build
profile-builder test
profile-builder package
```

Gate M4 : un utilisateur extérieur peut suivre le README sans connaître l'architecture du dépôt.

## M5 — premier GED prospectif

Choisir un GED nouveau et laisser le Builder produire le premier package candidat sans conception manuelle du processing plan.

Gate M5 : la décision machine est examinable, reproductible et bornée par le capability set.

## Règle de chantier

Ne pas augmenter l'automatisation tant que le contrat inférieur n'est pas observable et testable.