# Profile Builder 0.1.0 — independent test environment acceptance

## Purpose

Validate the distributable package on an **independent, anonymous and reproducible Linux environment**.

The repository must not record personal machine names, account names, home paths or other workstation identifiers.

## Reference environment characteristics

Minimum observed-compatible characteristics:

```text
OS_FAMILY=Linux
PYTHON=3.12.x observed compatible
NETWORK_REQUIRED=NO
EXTERNAL_PYTHON_PACKAGE_REQUIRED=NO
SYSTEM_SERVICE_MUTATION=NO
LLM_REQUIRED=NO
```

A different Linux distribution or Python patch version may be used; the observed environment is evidence, not a unique deployment target.

## Working directory

Use any local private working directory chosen by the tester, for example:

```text
<LOCAL_TEST_ROOT>/
```

The actual path is local evidence and must not be committed to the public repository.

## Preflight

```bash
cd "<LOCAL_TEST_ROOT>"
python3 --version
sha256sum ulisdoq-profile-builder-0.1.0.tar.gz
```

Expected archive SHA-256 for release 0.1.0:

```text
f82e610db48b8d894f702485ec0e7f9fc89599fd385105f19c1b75441fa7a66f
```

## Execution

```bash
tar -xzf ulisdoq-profile-builder-0.1.0.tar.gz
cd ulisdoq-profile-builder-0.1.0

./bin/profile-builder info
./bin/profile-builder selftest

./bin/profile-builder plan \
  --characterization examples/ged03/characterization.json \
  --need examples/ged03/requested_need.json \
  --output /tmp/ged03-plan.json

sha256sum /tmp/ged03-plan.json
cat /tmp/ged03-plan.json
```

## Gate

Required:

- `ged03_replay=PASS`
- `unknown_fail_closed=PASS`
- `overall=PASS`
- deterministic GED-03 plan stable
- no external Python package required
- no system mutation required

GED-04 may only be submitted prospectively after this gate.

`CAPABILITY_GAP` remains a valid first result.
