#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

python3 -m py_compile "$ROOT_DIR/scripts/semantic-svg-checks.py"
bash "$ROOT_DIR/scripts/test-templates.sh"
bash "$ROOT_DIR/scripts/test-examples.sh"
bash "$ROOT_DIR/scripts/test-generated-complex.sh"
bash "$ROOT_DIR/scripts/test-generated-stress.sh"
bash "$ROOT_DIR/scripts/test-semantic-negative.sh"

echo "PASS: architecture-diagram validation suite passed"
