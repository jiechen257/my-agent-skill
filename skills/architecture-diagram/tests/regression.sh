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

echo "Running template validation suite..."
bash "$SKILL_DIR/scripts/test-templates.sh" || fail "template validation suite failed"

echo "PASS: architecture-diagram regression checks"
