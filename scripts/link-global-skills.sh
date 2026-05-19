#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ROOT=$(cd -- "$SCRIPT_DIR/.." && pwd)
REGISTRY="$ROOT/registry/skills.yaml"
STAMP=$(date +%Y%m%d-%H%M%S)

list_skills() {
  awk '
    function emit() {
      if (name != "") {
        print name "|" path "|" kind "|" codex "|" claude
      }
    }
    /^[[:space:]]*-[[:space:]]name:/ {
      emit()
      name=$3
      path=kind=codex=claude=""
      next
    }
    /^[[:space:]]*path:/ { path=$2; next }
    /^[[:space:]]*kind:/ { kind=$2; next }
    /^[[:space:]]*codex:/ { codex=$2; next }
    /^[[:space:]]*claude:/ { claude=$2; next }
    END { emit() }
  ' "$REGISTRY"
}

backup_path() {
  local dest=$1
  local backup="${dest}.backup-${STAMP}"
  local index=1
  while [ -e "$backup" ] || [ -L "$backup" ]; do
    backup="${dest}.backup-${STAMP}-${index}"
    index=$((index + 1))
  done
  mv "$dest" "$backup"
  printf 'BACKUP %s -> %s\n' "$dest" "$backup"
}

link_one() {
  local manager=$1
  local root=$2
  local name=$3
  local target=$4
  local enabled=$5

  [ "$enabled" = "true" ] || return 0
  mkdir -p "$root"

  if [ ! -e "$target/SKILL.md" ]; then
    printf 'ERROR %s target missing: %s\n' "$name" "$target/SKILL.md" >&2
    return 1
  fi

  local dest="$root/$name"
  if [ -L "$dest" ] && [ "$(readlink "$dest")" = "$target" ]; then
    printf 'OK     %-6s %-28s -> %s\n' "$manager" "$name" "$target"
    return 0
  fi

  if [ -e "$dest" ] || [ -L "$dest" ]; then
    backup_path "$dest"
  fi

  ln -s "$target" "$dest"
  printf 'LINK   %-6s %-28s -> %s\n' "$manager" "$name" "$target"
}

while IFS='|' read -r name path kind codex claude; do
  [ -n "$name" ] || continue
  target="$ROOT/$path"
  link_one codex "$HOME/.codex/skills" "$name" "$target" "$codex"
  link_one claude "$HOME/.claude/skills" "$name" "$target" "$claude"
done < <(list_skills)
