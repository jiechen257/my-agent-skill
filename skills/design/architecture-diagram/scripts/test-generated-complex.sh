#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/scripts/validate-svg.sh"

GENERATED="$(find "$ROOT_DIR/tests/generated-complex" -maxdepth 1 -type f -name "*.svg" | sort)"

if [ -z "$GENERATED" ]; then
  echo "FAIL: no generated complex SVG files found" >&2
  exit 1
fi

while IFS= read -r diagram; do
  [ -n "$diagram" ] || continue
  bash "$VALIDATOR" "$diagram"
done <<EOF
$GENERATED
EOF

echo "PASS: all generated complex diagrams validated"
