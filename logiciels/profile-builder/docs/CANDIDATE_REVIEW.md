# Profile Builder — contrat de revue d'un profil candidat

**Référence :** PROFILE-BUILDER-CANDIDATE-REVIEW-CONTRACT-001
**Statut :** candidat

## 1. Objet

Permettre une revue éclairée, questionnée et traçable d'un profil candidat en quarantaine.

La revue peut être conduite par un humain, par un fil ChatGPT spécialisé, ou par un autre outil d'assistance, mais elle ne possède pas par défaut l'autorité de promulgation.

## 2. Principe

Chaque anomalie doit être :

```text
OBSERVED
→ CHARACTERIZED
→ EVIDENCED
→ IMPACTED
→ PROPOSED_ACTION
```

## 3. Objet minimal d'anomalie

Chaque finding doit contenir au minimum :

```text
finding_id
candidate_profile_id
candidate_profile_version
review_scope
severity
category
claim
evidence_refs
reproduction_steps
expected_behavior
observed_behavior
impact
confidence
proposed_action
status
```

## 4. Catégories

Catégories candidates :

- PRIVACY ;
- RECOGNITION ;
- EXTRACTION ;
- SEMANTICS ;
- BUSINESS_RULE ;
- ROBUSTNESS ;
- REPRODUCIBILITY ;
- DEPENDENCY ;
- SECURITY ;
- LICENSING ;
- DOCUMENTATION ;
- GENERALIZATION ;
- OTHER.

## 5. Sévérité

```text
BLOCKING
MAJOR
MINOR
OBSERVATION
```

`BLOCKING` signifie : le candidat ne doit pas être promulgué dans son état actuel.

## 6. Preuve

Un finding sans preuve explicite reste une hypothèse de revue.

Les preuves peuvent référencer :

- test reproductible ;
- fixture synthétique ;
- résultat de matcher ;
- sortie d'extraction minimisée ;
- hash ;
- comparaison ground truth ;
- violation de schéma ;
- contradiction documentaire ;
- règle métier versionnée ;
- preuve de fuite/privacy gate.

Les documents privés ne doivent pas être copiés dans la revue publique.

## 7. Cycle d'un finding

```text
OPEN
→ CONFIRMED | NOT_REPRODUCED | INVALID
→ CORRECTION_PROPOSED
→ FIXED_PENDING_RETEST
→ CLOSED
```

Un finding `BLOCKING` confirmé empêche la promulgation tant qu'il n'est pas fermé ou explicitement dérogé par l'autorité compétente.

## 8. Rôle possible d'un fil ChatGPT

Un fil spécialisé peut :

- lire le candidat et ses preuves ;
- poser des questions au contributeur ;
- rechercher des contradictions ;
- proposer des tests ;
- caractériser les anomalies ;
- produire des findings structurés ;
- vérifier qu'une correction répond au finding ;
- produire une synthèse de revue.

Il ne doit pas :

- inventer une preuve ;
- accéder à des documents privés non autorisés ;
- transformer une hypothèse en fait ;
- promulguer automatiquement le profil.

## 9. Sortie de revue

La revue produit :

```text
REVIEW_SUMMARY
FINDINGS[]
EVIDENCE_INDEX
OPEN_BLOCKERS
RECOMMENDATION
```

La recommandation n'est pas la décision d'autorité.

## 10. Gate vers promulgation

Conditions minimales candidates :

```text
PRIVACY_GATE=PASS
OPEN_BLOCKING_FINDINGS=0
REPRODUCIBILITY=PASS
REQUIRED_TESTS=PASS
HUMAN_AUTHORITY_DECISION=ACCEPTED
```