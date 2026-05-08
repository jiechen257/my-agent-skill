#!/usr/bin/env bash
set -euo pipefail

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SKILL_MD="$SKILL_DIR/SKILL.md"

fail() {
  echo "FAIL: $1" >&2
  exit 1
}

echo "Checking default output rules..."
grep -q "默认输出语言：中文" "$SKILL_MD" || fail "missing Chinese default guidance"
grep -q "默认风格：\`claude-official\`" "$SKILL_MD" || fail "missing claude-official default guidance"
grep -q "默认不生成 \`.html\`" "$SKILL_MD" || fail "missing no-html guidance"
grep -q "默认不生成 \`.png\`" "$SKILL_MD" || fail "missing no-png guidance"
grep -q "默认不在图内写出风格名称" "$SKILL_MD" || fail "missing no-style-metadata guidance"
SKILL_WORDS="$(wc -w < "$SKILL_MD" | tr -d ' ')"
[ "$SKILL_WORDS" -le 1300 ] || fail "SKILL.md too long; keep prompt surface compact"

echo "Checking supported diagram types..."
for type in architecture flowchart data-flow sequence state-machine timeline comparison-matrix use-case; do
  grep -q "\`$type\`" "$SKILL_MD" || fail "missing type in SKILL.md: $type"
done

echo "Checking references..."
for ref in \
  "$SKILL_DIR/references/diagram-type-matrix.md" \
  "$SKILL_DIR/references/style-claude-official.md" \
  "$SKILL_DIR/references/style-default.md" \
  "$SKILL_DIR/references/svg-layout-best-practices.md"; do
  [ -f "$ref" ] || fail "missing reference file: $ref"
done
grep -q "above the segment" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing edge label placement rule"
grep -q "branch-owned segment" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing branched trunk label ownership rule"
grep -q "segment is too short" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing short-segment reroute rule"
grep -q "message endpoints must land" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing message endpoint landing rule"
grep -q "activation bar must overlap" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing activation overlap rule"
grep -q "data-frame-id" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing frame semantic attribute rule"
grep -q "data-edge-id" "$SKILL_DIR/references/svg-layout-best-practices.md" || fail "missing edge label ownership attribute rule"
LAYOUT_WORDS="$(wc -w < "$SKILL_DIR/references/svg-layout-best-practices.md" | tr -d ' ')"
[ "$LAYOUT_WORDS" -le 1100 ] || fail "svg-layout-best-practices.md too long; keep reference compact"

echo "Checking scripts..."
for script in \
  "$SKILL_DIR/scripts/validate-svg.sh" \
  "$SKILL_DIR/scripts/test-templates.sh"; do
  [ -f "$script" ] || fail "missing script: $script"
done

echo "Checking templates..."
for template in \
  "$SKILL_DIR/assets/template.svg" \
  "$SKILL_DIR/assets/template-default.svg" \
  "$SKILL_DIR/assets/template-claude-official.svg" \
  "$SKILL_DIR/templates/architecture.svg" \
  "$SKILL_DIR/templates/flowchart.svg" \
  "$SKILL_DIR/templates/data-flow.svg" \
  "$SKILL_DIR/templates/sequence.svg" \
  "$SKILL_DIR/templates/state-machine.svg" \
  "$SKILL_DIR/templates/timeline.svg" \
  "$SKILL_DIR/templates/comparison-matrix.svg" \
  "$SKILL_DIR/templates/use-case.svg"; do
  [ -f "$template" ] || fail "missing template: $template"
done
! grep -q "claude-official 共用布局" "$SKILL_DIR/assets/template.svg" || fail "template.svg still exposes style metadata"

echo "Checking template placeholders..."
grep -q "\[系统名称\] 架构图" "$SKILL_DIR/templates/architecture.svg" || fail "architecture template missing placeholder"
grep -q "\[流程名称\] 流程图" "$SKILL_DIR/templates/flowchart.svg" || fail "flowchart template missing placeholder"
grep -q "\[交互主题\] 时序图" "$SKILL_DIR/templates/sequence.svg" || fail "sequence template missing placeholder"
grep -q "\[系统名称\] 用例图" "$SKILL_DIR/templates/use-case.svg" || fail "use-case template missing placeholder"
grep -q "data-edge-id" "$SKILL_DIR/templates/flowchart.svg" || fail "flowchart template missing edge label semantic attributes"
grep -q "data-edge-id" "$SKILL_DIR/templates/data-flow.svg" || fail "data-flow template missing edge label semantic attributes"
grep -q "id=\"edge-" "$SKILL_DIR/templates/architecture.svg" || fail "architecture template missing edge ids"
grep -q "data-edge-id" "$SKILL_DIR/templates/use-case.svg" || fail "use-case template missing relation label semantic attributes"
grep -q "data-frame-id" "$SKILL_DIR/templates/sequence.svg" || fail "sequence template missing semantic frame attributes"

echo "Running template validation suite..."
bash "$SKILL_DIR/scripts/test-templates.sh" || fail "template validation suite failed"

echo "Running semantic fixture suite..."
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/sequence-good.svg" || fail "good sequence fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/flowchart-good-edge-label.svg" || fail "good edge-label fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/common-good-text-fit.svg" || fail "good text-fit fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/common-good-node-fit.svg" || fail "good node-fit fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/common-good-cell-fit.svg" || fail "good cell-fit fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/usecase-good-relation-label.svg" || fail "good relation-label fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/common-good-container-spacing.svg" || fail "good container-spacing fixture failed"
bash "$SKILL_DIR/scripts/validate-svg.sh" "$SKILL_DIR/tests/fixtures/common-good-edge-clearance.svg" || fail "good edge-clearance fixture failed"
for bad_fixture in \
  "$SKILL_DIR/tests/fixtures/common-bad-chip-node-overlap.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-chip-chip-overlap.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-edge-node-clearance.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-edge-label-clearance.svg" \
  "$SKILL_DIR/tests/fixtures/usecase-bad-floating-relation-label.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-cell-label-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-bar-label-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-rect-node-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-ellipse-node-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-decision-node-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-chip-text-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-note-text-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-phase-text-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/common-bad-legend-text-overflow.svg" \
  "$SKILL_DIR/tests/fixtures/flowchart-bad-floating-chip.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-dangling-activation.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-short-lifeline.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-top-phase-band.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-legend-inset.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-note-inset.svg" \
  "$SKILL_DIR/tests/fixtures/sequence-bad-frame-branch.svg"; do
  if bash "$SKILL_DIR/scripts/validate-svg.sh" "$bad_fixture"; then
    fail "bad fixture unexpectedly passed: $bad_fixture"
  fi
done

echo "PASS: architecture-diagram regression checks"
