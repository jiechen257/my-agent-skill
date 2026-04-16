#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SVG_TEMPLATE="$SKILL_DIR/assets/template.svg"
CLAUDE_TEMPLATE="$SKILL_DIR/assets/template-claude.svg"
RSVG_BIN="$(command -v rsvg-convert || true)"

if [ -z "$RSVG_BIN" ] && [ -x /opt/homebrew/bin/rsvg-convert ]; then
  RSVG_BIN=/opt/homebrew/bin/rsvg-convert
fi

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

validate_svg_template() {
  local template_path="$1"
  local label="$2"

  test -f "$template_path" || fail "$label missing"
  test -n "$RSVG_BIN" || fail "rsvg-convert not found"

  TMP_PNG="$(mktemp /tmp/architecture-diagram-svg-XXXXXX.png)"
  "$RSVG_BIN" "$template_path" -o "$TMP_PNG" >/dev/null 2>&1 || fail "$label failed rsvg-convert validation"
  rm -f "$TMP_PNG"

  grep -q "\[项目名称\] 架构图" "$template_path" || fail "$label missing Chinese title placeholder"
  grep -q "edge-label-bg" "$template_path" || fail "$label missing label background class"
  grep -q "note-card" "$template_path" || fail "$label missing note-card class"
  grep -q "phase-pill" "$template_path" || fail "$label missing phase-pill class"
  grep -q "subpanel" "$template_path" || fail "$label missing subpanel example"
  grep -q "terminal-node" "$template_path" || fail "$label missing terminal-node class"
  grep -q "<tspan" "$template_path" || fail "$label missing wrapped note text"

  if grep -Eq 'd="[^"]*[CQ][^"]*"' "$template_path"; then
    fail "$label still contains curved path commands"
  fi
}

echo "Checking default Chinese output guidance..."
grep -q "默认使用中文" "$SKILL_MD" || fail "SKILL.md missing default Chinese output guidance"

echo "Checking supported styles guidance..."
grep -q "Supported Style Profiles" "$SKILL_MD" || fail "SKILL.md missing supported styles section"
grep -q "\`default\`" "$SKILL_MD" || fail "SKILL.md missing default style guidance"
grep -q "\`claude-official\`" "$SKILL_MD" || fail "SKILL.md missing claude-official style guidance"

echo "Checking standalone SVG guidance..."
grep -q "\.svg" "$SKILL_MD" || fail "SKILL.md missing standalone SVG guidance"

echo "Checking SVG-only output guidance..."
grep -q "Do not generate \`.html\` files by default" "$SKILL_MD" || fail "SKILL.md missing no-html default guidance"
grep -q "Do not generate \`.png\` files by default" "$SKILL_MD" || fail "SKILL.md missing no-png default guidance"

echo "Checking routed-edge guidance..."
grep -q "端口锚点" "$SKILL_MD" || fail "SKILL.md missing port anchor guidance"
grep -q "正交走线" "$SKILL_MD" || fail "SKILL.md missing orthogonal routing guidance"
grep -q "标签" "$SKILL_MD" || fail "SKILL.md missing label routing guidance"
grep -q "visible node port" "$SKILL_MD" || fail "SKILL.md missing visible node port guidance"
grep -q "opposite sides" "$SKILL_MD" || fail "SKILL.md missing opposite-side port guidance"
grep -q "corridor segment" "$SKILL_MD" || fail "SKILL.md missing corridor overlap guidance"

echo "Checking text-layout guidance..."
grep -q "note rail" "$SKILL_MD" || fail "SKILL.md missing note rail guidance"
grep -q "leader line" "$SKILL_MD" || fail "SKILL.md missing leader line guidance"
grep -q "<tspan>" "$SKILL_MD" || fail "SKILL.md missing tspan wrapping guidance"

echo "Checking region and shape guidance..."
grep -q "title pill" "$SKILL_MD" || fail "SKILL.md missing title pill guidance"
grep -q "shape vocabulary" "$SKILL_MD" || fail "SKILL.md missing shape vocabulary guidance"
grep -q "subpanel" "$SKILL_MD" || fail "SKILL.md missing subpanel guidance"

echo "Checking HTML template is absent..."
if [ -e "$SKILL_DIR/assets/template.html" ]; then
  fail "assets/template.html should not exist in SVG-only mode"
fi

echo "Validating default SVG template..."
validate_svg_template "$SVG_TEMPLATE" "template.svg"
grep -q "edge: user.right -> entry.left" "$SVG_TEMPLATE" || fail "template.svg missing explicit edge endpoint example"

echo "Validating claude SVG template..."
validate_svg_template "$CLAUDE_TEMPLATE" "template-claude.svg"
grep -q "edge: user.right -> gateway.left" "$CLAUDE_TEMPLATE" || fail "template-claude.svg missing explicit edge endpoint example"
grep -q "shadow-soft" "$CLAUDE_TEMPLATE" || fail "template-claude.svg missing claude shadow token"
grep -q "#f8f6f3" "$CLAUDE_TEMPLATE" || fail "template-claude.svg missing claude background token"

echo "PASS: architecture-diagram regression checks"
