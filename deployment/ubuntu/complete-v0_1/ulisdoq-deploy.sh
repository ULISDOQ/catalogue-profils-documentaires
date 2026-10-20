#!/usr/bin/env bash
set -euo pipefail

ACTION="${1:-}"
shift || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROFILE_ROOT="${ULISDOQ_PROFILE_ROOT:-$HOME/.local/share/ulisdoq/complete-v0_1}"
INSTALL_SYSTEM=NO

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) PROFILE_ROOT="$2"; shift 2 ;;
    --install-system) INSTALL_SYSTEM=YES; shift ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

VENVS="$PROFILE_ROOT/venvs"
EVIDENCE="$PROFILE_ROOT/evidence"
APT_FILE="$SCRIPT_DIR/apt-packages.txt"
VERIFY="$SCRIPT_DIR/verify_complete.py"

usage() {
  cat <<EOF
Usage:
  $0 install [--root PATH] [--install-system]
  $0 verify  [--root PATH]
  $0 rollback [--root PATH]

install-system is explicit because it invokes sudo apt-get.
EOF
}

require_source_identity() {
  git -C "$REPO_ROOT" rev-parse --is-inside-work-tree >/dev/null
  HEAD="$(git -C "$REPO_ROOT" rev-parse HEAD)"
  DIRTY="$(git -C "$REPO_ROOT" status --porcelain)"
  if [[ -n "$DIRTY" ]]; then
    echo "FAIL: source worktree is not clean" >&2
    exit 10
  fi
  echo "$HEAD" > "$EVIDENCE/source_commit.txt"
}

preflight_python() {
  PYTHON_BIN="${PYTHON_BIN:-python3}"
  "$PYTHON_BIN" - <<'PY'
import platform, sys
v=tuple(map(int, platform.python_version_tuple()))
if v < (3,12,3):
    raise SystemExit("Python >= 3.12.3 required for deployment attempt")
print(platform.python_version(), sys.executable)
PY
}

create_env() {
  local name="$1"
  local req="${2:-}"
  local target="$VENVS/$name"
  if [[ -e "$target" ]]; then
    echo "FAIL: refusing to mutate existing environment $target" >&2
    exit 11
  fi
  "${PYTHON_BIN:-python3}" -m venv "$target"
  "$target/bin/python" -m pip install --upgrade pip
  if [[ -n "$req" ]]; then
    "$target/bin/python" -m pip install -r "$SCRIPT_DIR/$req"
  fi
  "$target/bin/python" -m pip freeze | LC_ALL=C sort > "$EVIDENCE/lock-$name.txt"
  sha256sum "$EVIDENCE/lock-$name.txt" > "$EVIDENCE/lock-$name.sha256"
}

case "$ACTION" in
  install)
    mkdir -p "$VENVS" "$EVIDENCE"
    preflight_python
    require_source_identity

    uname -a > "$EVIDENCE/uname.txt"
    cat /etc/os-release > "$EVIDENCE/os-release.txt"
    "${PYTHON_BIN:-python3}" --version > "$EVIDENCE/python-base.txt" 2>&1

    if [[ "$INSTALL_SYSTEM" == "YES" ]]; then
      mapfile -t PKGS < <(grep -Ev '^[[:space:]]*(#|$)' "$APT_FILE")
      sudo apt-get update
      sudo apt-get install -y --no-install-recommends "${PKGS[@]}"
    else
      echo "SYSTEM_PACKAGES_NOT_MUTATED" > "$EVIDENCE/system-install.txt"
    fi

    create_env core
    create_env anchor_graph requirements-anchor_graph.txt
    create_env visual_keypoints requirements-visual_keypoints.txt
    create_env invoice2data requirements-invoice2data.txt
    create_env semantic_validation requirements-semantic_validation.txt

    "$VENVS/core/bin/python" "$VERIFY"       --repo-root "$REPO_ROOT"       --profile-root "$PROFILE_ROOT"       > "$EVIDENCE/verify-complete.json"

    cat "$EVIDENCE/verify-complete.json"
    ;;

  verify)
    mkdir -p "$EVIDENCE"
    "$VENVS/core/bin/python" "$VERIFY"       --repo-root "$REPO_ROOT"       --profile-root "$PROFILE_ROOT"
    ;;

  rollback)
    if [[ -d "$VENVS" ]]; then
      rm -rf "$VENVS"
    fi
    echo "Rollback removed only ULISDOQ profile-owned virtual environments."
    echo "Evidence kept at: $EVIDENCE"
    echo "System packages were not removed."
    ;;

  *)
    usage
    exit 2
    ;;
esac
