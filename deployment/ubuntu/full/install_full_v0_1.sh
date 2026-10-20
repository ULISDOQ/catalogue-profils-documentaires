#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
APT_FILE="$ROOT/deployment/ubuntu/full/apt-packages-v0_1.txt"
REQ_IN="$ROOT/deployment/ubuntu/full/requirements-full-v0_1.in"
VERIFY="$ROOT/deployment/ubuntu/full/verify_full_v0_1.py"
VENV="${1:-$HOME/.venvs/ulisdoq-full-v0_1}"
EVIDENCE_DIR="${2:-$ROOT/.runtime/ulisdoq-full-evidence}"

mkdir -p "$EVIDENCE_DIR"

if [[ "$(uname -s)" != "Linux" ]]; then
  echo "FAIL: Linux required" >&2
  exit 2
fi

PYTHON_BIN="${PYTHON_BIN:-python3}"
"$PYTHON_BIN" - <<'PY'
import platform, sys
v=tuple(map(int, platform.python_version_tuple()))
req=(3,12,3)
if v < req:
    raise SystemExit(f"Python >= 3.12.3 required; observed {platform.python_version()}")
print("PYTHON_PRECHECK=PASS", platform.python_version(), sys.executable)
PY

if [[ -e "$VENV" ]]; then
  echo "FAIL: refusing to mutate existing venv: $VENV" >&2
  exit 3
fi

echo "System packages declared by ULISDOQ:"
grep -Ev '^[[:space:]]*(#|$)' "$APT_FILE"

if [[ "${ULISDOQ_INSTALL_SYSTEM_PACKAGES:-NO}" == "YES" ]]; then
  sudo apt-get update
  mapfile -t APT_PKGS < <(grep -Ev '^[[:space:]]*(#|$)' "$APT_FILE")
  sudo apt-get install -y --no-install-recommends "${APT_PKGS[@]}"
else
  echo "SYSTEM_INSTALL=SKIPPED"
  echo "Set ULISDOQ_INSTALL_SYSTEM_PACKAGES=YES only after explicit authorization."
fi

"$PYTHON_BIN" -m venv "$VENV"
"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install -r "$REQ_IN"

"$VENV/bin/python" -m pip freeze | LC_ALL=C sort > "$EVIDENCE_DIR/requirements-full-resolved.txt"
sha256sum "$EVIDENCE_DIR/requirements-full-resolved.txt" > "$EVIDENCE_DIR/requirements-full-resolved.sha256"

"$VENV/bin/python" "$VERIFY" > "$EVIDENCE_DIR/verify-full.json"

echo "VENV=$VENV"
echo "RESOLVED_LOCK=$EVIDENCE_DIR/requirements-full-resolved.txt"
echo "VERIFY=$EVIDENCE_DIR/verify-full.json"
