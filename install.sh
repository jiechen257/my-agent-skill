#!/usr/bin/env bash
set -euo pipefail

# install.sh — Bootstrap skills from this repo to Claude Code and Codex
# Usage: git clone <repo> && cd my-agent-skill && ./install.sh
#
# Behavior:
#   - Creates symlinks in ~/.claude/skills/ and ~/.codex/skills/ for each skill
#   - Discovers any directory under skills/ that contains SKILL.md
#   - Optional: EXTRA_SKILL_ROOTS=/path/to/skills[:/path/to/other/skills] ./install.sh
#   - Idempotent: safe to run multiple times
#   - Skips: pithos-* (managed by Pithos), dogfooding (device-specific)

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"

CLAUDE_DST="$HOME/.claude/skills"
CODEX_DST="$HOME/.codex/skills"

SKIP_PATTERNS=("pithos-" "dogfooding")

should_skip() {
  local name="$1"
  for pattern in "${SKIP_PATTERNS[@]}"; do
    if [[ "$name" == ${pattern}* ]]; then
      return 0
    fi
  done
  return 1
}

link_skill() {
  local skill_dir="$1"
  local skill_name="$2"
  local dest_root="$3"
  local label="$4"

  local target="$dest_root/$skill_name"

  if [ -L "$target" ]; then
    local current
    current="$(readlink "$target")"
    if [ "$current" = "$skill_dir" ] || [ "$current" = "${skill_dir%/}" ]; then
      return 1  # already correct
    else
      echo "  UPDATE [$label]: $skill_name (was → $current)"
      rm "$target"
    fi
  elif [ -e "$target" ]; then
    echo "  WARN [$label]: $skill_name exists as regular directory, skipping"
    return 2
  fi

  ln -s "${skill_dir%/}" "$target"
  echo "  LINK [$label]: $skill_name → ${skill_dir%/}"
  return 0
}

skill_roots=("$SKILLS_SRC")
if [ -n "${EXTRA_SKILL_ROOTS:-}" ]; then
  IFS=':' read -r -a extra_roots <<< "$EXTRA_SKILL_ROOTS"
  for extra_root in "${extra_roots[@]}"; do
    [ -n "$extra_root" ] || continue
    skill_roots+=("$extra_root")
  done
fi

echo "Installing skills from:"
for skill_root in "${skill_roots[@]}"; do
  echo "  $skill_root"
done
echo ""

# Ensure target directories exist
mkdir -p "$CLAUDE_DST"
targets=("$CLAUDE_DST|claude")
if [ -d "$HOME/.codex" ]; then
  mkdir -p "$CODEX_DST"
  targets+=("$CODEX_DST|codex")
fi

installed=0
skipped=0

install_from_root() {
  local root="$1"

  if [ ! -d "$root" ]; then
    echo "  WARN: skill root not found, skipping: $root"
    return
  fi

  while IFS= read -r -d '' skill_file; do
    local skill_dir
    local skill_name
    skill_dir="$(dirname "$skill_file")"
    skill_name="$(basename "$skill_dir")"

    if should_skip "$skill_name"; then
      echo "  SKIP: $skill_name (excluded pattern)"
      ((skipped++))
      continue
    fi

    for entry in "${targets[@]}"; do
      dest_root="${entry%%|*}"
      label="${entry##*|}"
      link_skill "$skill_dir" "$skill_name" "$dest_root" "$label" && ((installed++)) || true
    done
  done < <(find "$root" -mindepth 2 -type f -name SKILL.md -print0 | sort -z)
}

for skill_root in "${skill_roots[@]}"; do
  install_from_root "$skill_root"
done

echo ""
echo "Done: $installed linked, $skipped skipped"

# Verify no broken symlinks
broken=0
for entry in "${targets[@]}"; do
  dest_root="${entry%%|*}"
  while IFS= read -r -d '' link; do
    if [ ! -e "$link" ]; then
      echo "  BROKEN: $link → $(readlink "$link")"
      ((broken++))
    fi
  done < <(find "$dest_root" -maxdepth 1 -type l -print0)
done

if [ "$broken" -gt 0 ]; then
  echo "WARNING: $broken broken symlink(s) detected"
else
  echo "All symlinks valid."
fi
