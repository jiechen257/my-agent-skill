#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/scripts/validate-svg.sh"

TEMPLATES=(
  "$ROOT_DIR/assets/template.svg"
  "$ROOT_DIR/assets/template-default.svg"
  "$ROOT_DIR/assets/template-claude-official.svg"
  "$ROOT_DIR/templates/architecture.svg"
  "$ROOT_DIR/templates/flowchart.svg"
  "$ROOT_DIR/templates/data-flow.svg"
  "$ROOT_DIR/templates/sequence.svg"
  "$ROOT_DIR/templates/state-machine.svg"
  "$ROOT_DIR/templates/timeline.svg"
  "$ROOT_DIR/templates/comparison-matrix.svg"
  "$ROOT_DIR/templates/use-case.svg"
)

for template in "${TEMPLATES[@]}"; do
  bash "$VALIDATOR" "$template"
done

echo "PASS: all templates validated"
