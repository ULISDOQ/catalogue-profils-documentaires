#!/usr/bin/env bash
set -euo pipefail

PROFILE_ID="ULISDOQ-COMPLETE-UBUNTU-V0.1"
ACTION="${1:-}"
shift || true

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
PROFILE_ROOT="${ULISDOQ_PROFILE_ROOT:-$HOME/.local/share/ulisdoq/complete-v0_1}"
INSTALL_SYSTEM=NO
declare -A ATTACHED=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --root) PROFILE_ROOT="$2"; shift 2 ;;
    --install-system) INSTALL_SYSTEM=YES; shift ;;
    --attach)
      spec="$2"; shift 2
      name="${spec%%=*}"; value="${spec#*=}"
      [[ "$name" != "$spec" && -n "$value" ]] || { echo "Invalid --attach NAME=PATH" >&2; exit 2; }
      ATTACHED["$name"]="$value"
      ;;
    *) echo "Unknown argument: $1" >&2; exit 2 ;;
  esac
done

VENVS="$PROFILE_ROOT/venvs"
EVIDENCE="$PROFILE_ROOT/evidence"
STATE="$PROFILE_ROOT/environments.tsv"
OWNER="$PROFILE_ROOT/.ulisdoq-profile-owner"
APT_FILE="$SCRIPT_DIR/apt-packages.txt"
VERIFY="$SCRIPT_DIR/verify_complete.py"

usage() {
  cat <<EOF
Usage:
  $0 install [--root PATH] [--install-system] [--attach NAME=VENV ...]
  $0 verify  [--root PATH] [--attach NAME=VENV ...]
  $0 rollback [--root PATH]

Known environment names:
  core anchor_graph visual_keypoints invoice2data semantic_validation profile_extraction

--attach explicitly binds a pre-existing compatible venv.
Only missing environments are installed.
--install-system installs only missing APT packages and requires explicit authorization.
EOF
}

ensure_root_marker() {
  mkdir -p "$PROFILE_ROOT" "$VENVS" "$EVIDENCE"
  if [[ -e "$OWNER" ]]; then
    grep -qx "$PROFILE_ID" "$OWNER" || { echo "FAIL: profile root owned by another profile" >&2; exit 20; }
  else
    printf '%s\n' "$PROFILE_ID" > "$OWNER"
  fi
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

env_python() {
  local p="$1"
  [[ -x "$p/bin/python" ]] || { echo "FAIL: no executable $p/bin/python" >&2; return 1; }
  printf '%s\n' "$p/bin/python"
}

record_env() {
  local name="$1" mode="$2" target="$3"
  grep -v "^$name|" "$STATE" 2>/dev/null > "$STATE.tmp" || true
  printf '%s|%s|%s\n' "$name" "$mode" "$target" >> "$STATE.tmp"
  mv "$STATE.tmp" "$STATE"
}

ensure_env() {
  local name="$1" req="${2:-}"
  local target="$VENVS/$name"

  if [[ -n "${ATTACHED[$name]:-}" ]]; then
    target="${ATTACHED[$name]}"
    env_python "$target" >/dev/null
    record_env "$name" attached "$target"
    echo "ENV_$name=ATTACHED:$target"
    return
  fi

  if [[ -d "$target" ]]; then
    [[ -f "$target/.ulisdoq-owned" ]] || {
      echo "FAIL: existing unowned environment $target; use --attach $name=PATH explicitly" >&2
      exit 21
    }
    grep -qx "$PROFILE_ID:$name" "$target/.ulisdoq-owned" || {
      echo "FAIL: ownership marker mismatch for $target" >&2
      exit 22
    }
    env_python "$target" >/dev/null
    record_env "$name" owned "$target"
    echo "ENV_$name=REUSED_OWNED:$target"
    return
  fi

  "${PYTHON_BIN:-python3}" -m venv "$target"
  printf '%s:%s\n' "$PROFILE_ID" "$name" > "$target/.ulisdoq-owned"
  "$target/bin/python" -m pip install --upgrade pip
  if [[ -n "$req" ]]; then
    "$target/bin/python" -m pip install -r "$SCRIPT_DIR/$req"
  fi
  "$target/bin/python" -m pip freeze | LC_ALL=C sort > "$EVIDENCE/lock-$name.txt"
  sha256sum "$EVIDENCE/lock-$name.txt" > "$EVIDENCE/lock-$name.sha256"
  record_env "$name" owned "$target"
  echo "ENV_$name=INSTALLED:$target"
}

install_missing_system_packages() {
  mapfile -t PKGS < <(grep -Ev '^[[:space:]]*(#|$)' "$APT_FILE")
  missing=()
  for pkg in "${PKGS[@]}"; do
    dpkg-query -W -f='${Status}' "$pkg" 2>/dev/null | grep -q "ok installed" || missing+=("$pkg")
  done
  printf '%s\n' "${missing[@]:-}" > "$EVIDENCE/missing-system-packages-before.txt"
  if [[ "${#missing[@]}" -eq 0 ]]; then
    echo "SYSTEM_PACKAGES=ALREADY_PRESENT"
  elif [[ "$INSTALL_SYSTEM" == "YES" ]]; then
    sudo apt-get update
    sudo apt-get install -y --no-install-recommends "${missing[@]}"
  else
    echo "SYSTEM_PACKAGES_MISSING=${missing[*]}" >&2
    echo "Re-run with --install-system only if explicitly authorized." >&2
    exit 23
  fi
}

verify_cmd() {
  args=(--repo-root "$REPO_ROOT" --profile-root "$PROFILE_ROOT")
  while IFS='|' read -r name mode target; do
    [[ -n "$name" ]] || continue
    args+=(--env "$name=$target")
  done < "$STATE"
  "${PYTHON_BIN:-python3}" "$VERIFY" "${args[@]}"
}

case "$ACTION" in
  install)
    ensure_root_marker
    preflight_python
    require_source_identity
    uname -a > "$EVIDENCE/uname.txt"
    cat /etc/os-release > "$EVIDENCE/os-release.txt"
    "${PYTHON_BIN:-python3}" --version > "$EVIDENCE/python-base.txt" 2>&1

    install_missing_system_packages

    ensure_env core
    ensure_env anchor_graph requirements-anchor_graph.txt
    ensure_env visual_keypoints requirements-visual_keypoints.txt
    ensure_env invoice2data requirements-invoice2data.txt
    ensure_env semantic_validation requirements-semantic_validation.txt
    ensure_env profile_extraction requirements-profile_extraction.txt

    verify_cmd > "$EVIDENCE/verify-complete.json"
    cat "$EVIDENCE/verify-complete.json"
    ;;

  verify)
    ensure_root_marker
    require_source_identity
    [[ -f "$STATE" ]] || { echo "FAIL: no environment state at $STATE" >&2; exit 24; }
    verify_cmd
    ;;

  rollback)
    [[ -f "$OWNER" ]] || { echo "FAIL: ownership marker missing; rollback refused" >&2; exit 30; }
    grep -qx "$PROFILE_ID" "$OWNER" || { echo "FAIL: ownership marker mismatch; rollback refused" >&2; exit 31; }
    [[ -f "$STATE" ]] || { echo "FAIL: environment state missing; rollback refused" >&2; exit 32; }

    while IFS='|' read -r name mode target; do
      [[ "$mode" == "owned" ]] || continue
      [[ "$target" == "$PROFILE_ROOT/"* ]] || { echo "FAIL: owned path escapes profile root: $target" >&2; exit 33; }
      marker="$target/.ulisdoq-owned"
      [[ -f "$marker" ]] || { echo "FAIL: env ownership marker missing: $target" >&2; exit 34; }
      grep -qx "$PROFILE_ID:$name" "$marker" || { echo "FAIL: env ownership mismatch: $target" >&2; exit 35; }
      rm -rf "$target"
      echo "REMOVED_OWNED_ENV=$name:$target"
    done < "$STATE"

    echo "Attached environments were preserved."
    echo "Evidence preserved at $EVIDENCE"
    echo "System packages were not removed."
    ;;

  *)
    usage
    exit 2
    ;;
esac
