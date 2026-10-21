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

# The registry covers repository-owned skills; other installers also maintain
# global discovery directories. Catch dangling links without following caches.
python3 - "$SCRIPT_DIR/audit-skill-references.py" <<'PY_AUDIT' || status=1
from pathlib import Path
import re
import runpy
import sys
discover_entries = runpy.run_path(sys.argv[1])["discover_entries"]
home = Path.home()
roots = [home / relative for relative in (
    ".codex/skills", ".agents/skills", ".claude/skills", ".cursor/skills",
    ".gemini/skills", ".gemini/antigravity/global_skills",
    ".config/opencode/skills", ".opencode/skills", ".qoder/skills",
)]
failed = False
for root in roots:
    if not root.is_dir():
        continue
    broken = [entry for entry in root.iterdir()
              if entry.is_symlink() and not entry.exists()]
    for entry in broken:
        print(f"FAIL dangling skill: {entry}")
    failed |= bool(broken)
    print(f"{'FAIL' if broken else 'OK  '} global skills: {root}")
# Codex loads both personal and shared entries. Same canonical SKILL.md is
# legitimate sharing; the same name in separate source files is ambiguous.
names = {}
for root in roots[:2]:
    if not root.is_dir():
        continue
    for skill in discover_entries(root):
        if not skill.is_file():
            continue
        text = skill.read_text(encoding="utf-8")
        match = re.search(r"^name:\s*[\"']?([^\"'\n]+)", text, re.MULTILINE)
        if match:
            names.setdefault(match.group(1).strip(), set()).add(skill.resolve())
for name, files in names.items():
    if len(files) > 1:
        print(f"FAIL duplicate skill name: {name}: {', '.join(map(str, sorted(files)))}")
        failed = True
raise SystemExit(1 if failed else 0)
PY_AUDIT

# Exercise the paths Codex actually receives, including chained shared links,
# wrapper bodies and recursively linked references/scripts/assets.
python3 "$SCRIPT_DIR/audit-skill-references.py" || status=1

exit "$status"
