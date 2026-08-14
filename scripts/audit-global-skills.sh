#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
REGISTRY="$ROOT/registry/skills.yaml"

list_skills() {
  awk '
    function emit() {
      if (name != "") {
        print name "|" path "|" kind "|" codex "|" claude "|" source_type
      }
    }
    /^[[:space:]]*-[[:space:]]name:/ {
      emit()
      name=$3
      path=kind=codex=claude=source_type=""
      next
    }
    /^[[:space:]]*path:/ { path=$2; next }
    /^[[:space:]]*kind:/ { kind=$2; next }
    /^[[:space:]]*codex:/ { codex=$2; next }
    /^[[:space:]]*claude:/ { claude=$2; next }
    /^[[:space:]]*source_type:/ { source_type=$2; next }
    END { emit() }
  ' "$REGISTRY"
}

check_link() {
  local manager=$1
  local root=$2
  local name=$3
  local target=$4
  local enabled=$5

  [ "$enabled" = "true" ] || return 0

  local dest="$root/$name"
  if [ ! -e "$target/SKILL.md" ]; then
    if [ -d "$target" ]; then
      printf 'SKIP %-6s %-28s sync source: %s\n' "$manager" "$name" "$target"
      return 0
    fi
    printf 'FAIL %-6s %-28s target missing: %s\n' "$manager" "$name" "$target/SKILL.md"
    return 1
  fi

  if [ -L "$dest" ]; then
    local actual
    actual=$(readlink "$dest")
    if [ "$actual" = "$target" ]; then
      printf 'OK   %-6s %-28s -> %s\n' "$manager" "$name" "$target"
      return 0
    fi
    printf 'FAIL %-6s %-28s points to %s, expected %s\n' "$manager" "$name" "$actual" "$target"
    return 1
  fi

  if [ -e "$dest" ]; then
    printf 'FAIL %-6s %-28s exists but is not a symlink: %s\n' "$manager" "$name" "$dest"
    return 1
  fi

  printf 'FAIL %-6s %-28s missing: %s\n' "$manager" "$name" "$dest"
  return 1
}

status=0
while IFS='|' read -r name path kind codex claude source_type; do
  [ -n "$name" ] || continue
  target="$ROOT/$path"
  check_link codex "$HOME/.codex/skills" "$name" "$target" "$codex" || status=1
  check_link claude "$HOME/.claude/skills" "$name" "$target" "$claude" || status=1
done < <(list_skills)

exit "$status"
