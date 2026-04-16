#!/usr/bin/env bash
set -euo pipefail

if [ $# -ne 1 ]; then
  echo "Usage: $0 <svg-file>" >&2
  exit 1
fi

SVG_FILE="$1"
RSVG_BIN="$(command -v rsvg-convert || true)"

if [ -z "$RSVG_BIN" ] && [ -x /opt/homebrew/bin/rsvg-convert ]; then
  RSVG_BIN=/opt/homebrew/bin/rsvg-convert
fi

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

[ -f "$SVG_FILE" ] || fail "file not found: $SVG_FILE"
[ -n "$RSVG_BIN" ] || fail "rsvg-convert not found"

if command -v xmllint >/dev/null 2>&1; then
  xmllint --noout "$SVG_FILE" >/dev/null 2>&1 || fail "xmllint validation failed: $SVG_FILE"
fi

grep -q "</svg>" "$SVG_FILE" || fail "missing </svg> tag: $SVG_FILE"

python3 - "$SVG_FILE" <<'PY'
from pathlib import Path
import re
import sys

text = Path(sys.argv[1]).read_text(encoding='utf-8')

marker_refs = set(re.findall(r'marker-end="url\(#([^)]+)\)"', text))
marker_defs = set(re.findall(r'<marker id="([^"]+)"', text))
missing = sorted(marker_refs - marker_defs)
if missing:
    raise SystemExit(f"missing marker definitions: {', '.join(missing)}")

if re.search(r'd="[^"]*[CQ][^"]*"', text):
    raise SystemExit("curved path commands found; keep routed paths explicit in templates")
PY

TMP_PNG="$(mktemp /tmp/architecture-diagram-validate-XXXXXX.png)"
"$RSVG_BIN" "$SVG_FILE" -o "$TMP_PNG" >/dev/null 2>&1 || fail "rsvg-convert failed: $SVG_FILE"
rm -f "$TMP_PNG"

echo "PASS: $SVG_FILE"
