#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
VALIDATOR="$ROOT_DIR/scripts/validate-svg.sh"
TMP_DIR="$(mktemp -d -t architecture-diagram-negative)"

cleanup() {
  rm -rf "$TMP_DIR"
}
trap cleanup EXIT

expect_fail() {
  local name="$1"
  local svg_file="$2"
  local expected="$3"
  local output

  if output="$(bash "$VALIDATOR" "$svg_file" 2>&1)"; then
    echo "FAIL: $name unexpectedly passed" >&2
    exit 1
  fi

  if ! printf '%s\n' "$output" | grep -Fq "$expected"; then
    echo "FAIL: $name failed for the wrong reason" >&2
    printf '%s\n' "$output" >&2
    exit 1
  fi

  echo "PASS: $name rejected"
}

mutate() {
  local source="$1"
  local target="$2"
  local before="$3"
  local after="$4"

  python3 - "$source" "$target" "$before" "$after" <<'PY'
from pathlib import Path
import sys

source = Path(sys.argv[1])
target = Path(sys.argv[2])
before = sys.argv[3]
after = sys.argv[4]

text = source.read_text(encoding="utf-8")
if before not in text:
    raise SystemExit(f"mutation pattern not found: {before}")
target.write_text(text.replace(before, after, 1), encoding="utf-8")
PY
}

FLOW_BAD="$TMP_DIR/flowchart-floating-start.svg"
mutate \
  "$ROOT_DIR/examples/flowchart.svg" \
  "$FLOW_BAD" \
  '<path d="M 382 508 H 250 V 706 H 390 V 760" class="edge" id="edge-decision-no"/>' \
  '<path d="M 370 508 H 250 V 706 H 390 V 760" class="edge" id="edge-decision-no"/>'
expect_fail "floating flowchart branch start" "$FLOW_BAD" "does not start on a node border"

MATRIX_BAD="$TMP_DIR/matrix-missing-corner.svg"
mutate \
  "$ROOT_DIR/examples/comparison-matrix.svg" \
  "$MATRIX_BAD" \
  '  <rect x="60" y="150" width="120" height="50" class="header"/>
' \
  ''
expect_fail "missing comparison matrix corner" "$MATRIX_BAD" "missing the top-left header cell"

DATA_BAD="$TMP_DIR/data-flow-floating-end.svg"
mutate \
  "$ROOT_DIR/examples/data-flow.svg" \
  "$DATA_BAD" \
  '<path d="M 710 380 V 500 H 410 V 560" class="edge" id="edge-store-feedback"/>' \
  '<path d="M 710 380 V 500 H 410 V 540" class="edge" id="edge-store-feedback"/>'
expect_fail "floating data-flow feedback end" "$DATA_BAD" "does not end on a node border"

USE_CASE_BAD="$TMP_DIR/use-case-floating-relation-end.svg"
mutate \
  "$ROOT_DIR/examples/use-case.svg" \
  "$USE_CASE_BAD" \
  '<path d="M 550 470 H 580 V 396" class="edge relation" id="edge-extend"/>' \
  '<path d="M 550 470 H 580 V 420" class="edge relation" id="edge-extend"/>'
expect_fail "floating use-case relation end" "$USE_CASE_BAD" "does not end on a node border"

ARCH_DOGLEG_BAD="$TMP_DIR/architecture-short-dogleg.svg"
mutate \
  "$ROOT_DIR/tests/generated-stress/multi-tenant-agent-platform-architecture.svg" \
  "$ARCH_DOGLEG_BAD" \
  '<path d="M 220 245 V 390" class="edge" id="edge-slack-auth" data-from="slack" data-to="auth"/>' \
  '<path d="M 220 245 V 320 H 230 V 390" class="edge" id="edge-slack-auth" data-from="slack" data-to="auth"/>'
expect_fail "short architecture dogleg" "$ARCH_DOGLEG_BAD" "uses a short dogleg"

ARCH_FANOUT_BAD="$TMP_DIR/architecture-stacked-fanout.svg"
mutate \
  "$ROOT_DIR/tests/generated-stress/multi-tenant-agent-platform-architecture.svg" \
  "$ARCH_FANOUT_BAD" \
  '<path d="M 1190 425 H 1290" class="edge" id="edge-policy-dispatcher" data-from="policy" data-to="dispatcher"/>' \
  '<path d="M 1190 425 H 1290" class="edge" id="edge-policy-dispatcher" data-from="policy" data-to="dispatcher"/>
  <path d="M 1390 460 V 565 H 350 V 660" class="edge" id="edge-dispatcher-sandbox" data-from="dispatcher" data-to="sandbox"/>
  <path d="M 1390 460 V 550 H 670 V 660" class="edge" id="edge-dispatcher-connectors" data-from="dispatcher" data-to="connectors"/>
  <path d="M 1390 460 V 535 H 990 V 660" class="edge" id="edge-dispatcher-workflow" data-from="dispatcher" data-to="workflow"/>
  <path d="M 1390 460 V 565 H 1310 V 660" class="edge" id="edge-dispatcher-notify" data-from="dispatcher" data-to="notify"/>'
expect_fail "stacked architecture fan-out" "$ARCH_FANOUT_BAD" "uses stacked fan-out doglegs"

ARCH_UPWARD_BAD="$TMP_DIR/architecture-upward-entry.svg"
mutate \
  "$ROOT_DIR/tests/generated-stress/openclaw-feature-map.svg" \
  "$ARCH_UPWARD_BAD" \
  '<path d="M 590 466 V 568" class="edge" id="edge-agent-core-capability-bus" data-from="agent-core" data-to="capability-bus"/>' \
  '<path d="M 590 466 V 568" class="edge" id="edge-agent-core-capability-bus" data-from="agent-core" data-to="capability-bus"/>
  <path d="M 590 466 V 525 H 1250 V 466" class="edge" id="edge-agent-core-model-gateway" data-from="agent-core" data-to="model-gateway"/>'
expect_fail "upward architecture entry" "$ARCH_UPWARD_BAD" "enters the target upward"

echo "PASS: semantic negative checks rejected expected regressions"
