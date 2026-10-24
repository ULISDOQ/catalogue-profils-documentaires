# ULISDOQ — reference test environment policy

ULISDOQ records **reproducible technical characteristics**, not identities of contributors' personal machines.

## Public repository may record

- OS family and relevant version range;
- runtime versions;
- dependency versions and lock hashes;
- CPU architecture when technically relevant;
- memory or accelerator requirements when technically relevant;
- network requirement: yes/no;
- required system capabilities;
- package hashes;
- test commands using placeholders;
- pass/fail results and deterministic output hashes.

## Public repository must not record

- personal host names;
- personal account names;
- home directory paths;
- LAN addresses or private topology;
- device serial numbers;
- personal mount points;
- workstation-specific identifiers not required for reproduction.

Use placeholders such as:

```text
<LOCAL_TEST_ROOT>
<PRIVATE_CORPUS_ROOT>
<OUTPUT_ROOT>
```

Machine-specific operational records belong outside ULISDOQ, in the operator's private governance/operations system.

## Principle

```text
REPRODUCIBLE_CHARACTERISTICS=PUBLIC_OK
PERSONAL_MACHINE_IDENTITY=PRIVATE
```


## Git history hygiene

Removing or renaming a file in the current tree does not remove its previous contents from Git history.

If a personal machine identifier, private path or other non-public operational detail is committed by mistake:

1. stop treating the repository history as publication-safe;
2. remove the information from the current tree;
3. rewrite/purge the affected Git history before public release when confidentiality requires it;
4. re-check the rewritten history before publication.

Public-project review must therefore cover both the current tree and relevant Git history.
