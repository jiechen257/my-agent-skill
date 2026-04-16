#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
SVG_TEMPLATE="$SKILL_DIR/assets/template.svg"
RSVG_BIN="$(command -v rsvg-convert || true)"

if [ -z "$RSVG_BIN" ] && [ -x /opt/homebrew/bin/rsvg-convert ]; then
  RSVG_BIN=/opt/homebrew/bin/rsvg-convert
fi

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

echo "Checking default Chinese output guidance..."
grep -q "默认使用中文" "$SKILL_MD" || fail "SKILL.md missing default Chinese output guidance"

echo "Checking standalone SVG guidance..."
grep -q "\.svg" "$SKILL_MD" || fail "SKILL.md missing standalone SVG guidance"

echo "Checking SVG-only output guidance..."
grep -q "Do not generate \`.html\` files by default" "$SKILL_MD" || fail "SKILL.md missing no-html default guidance"
grep -q "Do not generate \`.png\` files by default" "$SKILL_MD" || fail "SKILL.md missing no-png default guidance"

echo "Checking routed-edge guidance..."
grep -q "端口锚点" "$SKILL_MD" || fail "SKILL.md missing port anchor guidance"
grep -q "正交走线" "$SKILL_MD" || fail "SKILL.md missing orthogonal routing guidance"
grep -q "标签" "$SKILL_MD" || fail "SKILL.md missing label routing guidance"

echo "Checking HTML template is absent..."
if [ -e "$SKILL_DIR/assets/template.html" ]; then
  fail "assets/template.html should not exist in SVG-only mode"
fi

echo "Checking SVG template exists..."
test -f "$SVG_TEMPLATE" || fail "assets/template.svg missing"

echo "Validating SVG template..."
test -n "$RSVG_BIN" || fail "rsvg-convert not found"
TMP_PNG="$(mktemp /tmp/architecture-diagram-svg-XXXXXX.png)"
"$RSVG_BIN" "$SVG_TEMPLATE" -o "$TMP_PNG" >/dev/null 2>&1 || fail "template.svg failed rsvg-convert validation"
rm -f "$TMP_PNG"

echo "Checking SVG template defaults to Chinese..."
grep -q "\[项目名称\] 架构图" "$SVG_TEMPLATE" || fail "template.svg missing Chinese title placeholder"
grep -q "edge-label-bg" "$SVG_TEMPLATE" || fail "template.svg missing label background class"
if grep -Eq 'd="[^"]*[CQ][^"]*"' "$SVG_TEMPLATE"; then
  fail "template.svg still contains curved path commands"
fi

echo "PASS: architecture-diagram regression checks"
