#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/scripts/validate-svg.sh"

EXAMPLES="$(find "$ROOT_DIR/examples" -maxdepth 1 -type f -name "*.svg" | sort)"

if [ -z "$EXAMPLES" ]; then
  echo "FAIL: no example SVG files found" >&2
  exit 1
fi

while IFS= read -r example; do
  [ -n "$example" ] || continue
  bash "$VALIDATOR" "$example"
done <<EOF
$EXAMPLES
EOF

echo "PASS: all examples validated"
