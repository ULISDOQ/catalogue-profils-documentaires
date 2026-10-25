# ULISDOQ — Escalade consommateur v1

Statut : contrat candidat, premier cas probant GED-04.

## Objet

Ce répertoire porte le contrat Git générique utilisé par tout consommateur ULISDOQ lorsque le catalogue ou les capacités disponibles ne suffisent pas à traiter correctement un cas documentaire.

Le protocole est volontairement indépendant de CLAU.

```text
consumer
  -> request.json
  -> ULISDOQ receipt.json
  -> documentary instruction
  -> result.json
  -> consumer re-entry
```

Git is the versioned exchange surface. Publication of a request is not acceptance.

## Canonical paths

```text
escalade-consommateur/
  schemas/
    consumer-request-v1.schema.json
    consumer-receipt-v1.schema.json
    documentary-instruction-v1.schema.json
  demandes/<request_id>/request.json
  accuses/<request_id>/receipt.json
  resultats/<request_id>/result.json
  bin/ulisdoq-escalation
  tests/test_contract_v1.py
```

Objects are never moved to represent lifecycle. Request identity stays stable; receipt and result add lifecycle evidence.

## Request lifecycle

```text
PUBLISHED
  -> ACQUIRED
  -> ACCEPTED | REJECTED_* | UNKNOWN
  -> DOCUMENTARY_INSTRUCTION
  -> COMPLETED | NEEDS_MORE_EVIDENCE | INSUFFICIENT_EVIDENCE | UNSUPPORTED | UNKNOWN
  -> CONSUMER_REENTRY
```

## Privacy boundary

The default Git request MUST NOT contain:
- source document;
- observed private values;
- private local paths;
- private hashes;
- raw OCR;
- private ground truth.

If source evidence is needed, the result requests the minimum additional evidence and its acceptable representation. Public Git remains non-private by default.

## Idempotence

Processing identity is:

```text
request_id + request_version + request_commit
```

An already accepted/processed request version is not productively reprocessed. An uncertain state is returned as UNKNOWN; no blind retry is allowed.

## Consumer re-entry

A completed result MUST provide one explicit next action:

- USE_PROFILE
- USE_CAPABILITY
- RETRY_WITH_VERSION
- PROVIDE_ADDITIONAL_EVIDENCE
- STOP_INSUFFICIENT_EVIDENCE
- STOP_UNSUPPORTED

The consumer must not need to inspect ULISDOQ internal changelogs to continue.

## First proof

GED-04 is the first real protocol proof. The fixture contains only minimized, non-sensitive characterization and existing public/version references. It contains no source PDF or private values.

Success means the originating consumer can determine its next action from result.json alone.
