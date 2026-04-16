#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"
HTML_TEMPLATE="$SKILL_DIR/assets/template.html"
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

echo "Checking routed-edge guidance..."
grep -q "端口锚点" "$SKILL_MD" || fail "SKILL.md missing port anchor guidance"
grep -q "正交走线" "$SKILL_MD" || fail "SKILL.md missing orthogonal routing guidance"
grep -q "标签" "$SKILL_MD" || fail "SKILL.md missing label routing guidance"

echo "Checking HTML template does not rely on horizontal scroll..."
if grep -q "overflow-x: auto" "$HTML_TEMPLATE"; then
  fail "template.html still relies on overflow-x auto"
fi

echo "Checking HTML template does not force min-width clipping..."
if grep -q "min-width:" "$HTML_TEMPLATE"; then
  fail "template.html still contains min-width"
fi

echo "Checking HTML template defaults to Chinese..."
grep -q 'lang="zh-CN"' "$HTML_TEMPLATE" || fail "template.html missing zh-CN language tag"
grep -q "\[项目名称\] 架构图" "$HTML_TEMPLATE" || fail "template.html missing Chinese title placeholder"
grep -q "不透明底" "$HTML_TEMPLATE" || fail "template.html missing label background guidance"
if grep -Eq 'd="[^"]*[CQ][^"]*"' "$HTML_TEMPLATE"; then
  fail "template.html still contains curved path commands"
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
