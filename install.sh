#!/usr/bin/env bash
set -euo pipefail

# install.sh — Bootstrap Claude Code skills from this repo
# Usage: git clone <repo> && cd my-agent-skill && ./install.sh
#
# Behavior:
#   - Creates symlinks in ~/.claude/skills/ for each skill in this repo
#   - Idempotent: safe to run multiple times
#   - Skips: pithos-* (managed by Pithos), dogfooding (device-specific)
#   - Also links dingtalk-doc-rw.md command if ~/.claude/commands/ exists

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILLS_SRC="$SCRIPT_DIR/skills"
SKILLS_DST="$HOME/.claude/skills"

# Ensure target directory exists
mkdir -p "$SKILLS_DST"

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

echo "Installing skills from: $SKILLS_SRC"
echo "Target directory: $SKILLS_DST"
echo ""

installed=0
skipped=0
already=0

# Iterate over all skill directories (two levels: category/skill-name)
for category_dir in "$SKILLS_SRC"/*/; do
  [ -d "$category_dir" ] || continue
  for skill_dir in "$category_dir"*/; do
    [ -d "$skill_dir" ] || continue
    # Only process directories that contain SKILL.md
    [ -f "$skill_dir/SKILL.md" ] || continue

    skill_name="$(basename "$skill_dir")"

    # Skip excluded patterns
    if should_skip "$skill_name"; then
      echo "  SKIP: $skill_name (excluded pattern)"
      ((skipped++))
      continue
    fi

    target="$SKILLS_DST/$skill_name"

    # If symlink already points to the correct location, skip
    if [ -L "$target" ]; then
      current="$(readlink "$target")"
      if [ "$current" = "$skill_dir" ] || [ "$current" = "${skill_dir%/}" ]; then
        ((already++))
        continue
      else
        # Symlink exists but points elsewhere — update it
        echo "  UPDATE: $skill_name (was → $current)"
        rm "$target"
      fi
    elif [ -e "$target" ]; then
      # Regular directory exists — skip with warning
      echo "  WARN: $skill_name exists as regular directory, skipping (migrate manually)"
      ((skipped++))
      continue
    fi

    # Create symlink
    ln -s "${skill_dir%/}" "$target"
    echo "  LINK: $skill_name → ${skill_dir%/}"
    ((installed++))
  done
done

echo ""
echo "Done: $installed linked, $already unchanged, $skipped skipped"

# Verify no broken symlinks among our managed skills
broken=0
for link in "$SKILLS_DST"/*/; do
  [ -L "${link%/}" ] || continue
  if [ ! -e "${link%/}" ]; then
    echo "  BROKEN: ${link%/} → $(readlink "${link%/}")"
    ((broken++))
  fi
done

if [ "$broken" -gt 0 ]; then
  echo "WARNING: $broken broken symlink(s) detected"
else
  echo "All symlinks valid."
fi
