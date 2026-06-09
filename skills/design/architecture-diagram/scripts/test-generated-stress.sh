#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/scripts/validate-svg.sh"

STRESS_SET="$(find "$ROOT_DIR/tests/generated-stress" -maxdepth 1 -type f -name "*.svg" | sort)"

if [ -z "$STRESS_SET" ]; then
  echo "FAIL: no generated stress SVG files found" >&2
  exit 1
fi

while IFS= read -r diagram; do
  [ -n "$diagram" ] || continue
  bash "$VALIDATOR" "$diagram"
done <<EOF
$STRESS_SET
EOF

echo "PASS: all generated stress diagrams validated"
