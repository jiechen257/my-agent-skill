---
name: architecture-diagram
description: Use when the user asks for architecture diagrams, technical flowcharts, data-flow diagrams, sequence diagrams, state-machine diagrams, timelines, comparison matrices, use-case diagrams, or framework principle diagrams as standalone SVG deliverables.
---

# Architecture Diagram

Create production-grade technical diagrams as standalone SVG files.

Supported types:

- `architecture`
- `flowchart`
- `data-flow`
- `sequence`
- `state-machine`
- `timeline`
- `comparison-matrix`
- `use-case`

Supported styles:

- `default`
- `claude-official`

## Output Defaults

- 默认输出语言：中文
- 默认风格：`claude-official`
- 默认主题：light
- 默认交付物：单个 `.svg`
- 默认不生成 `.html`
- 默认不生成 `.png`
- 默认不在图内写出风格名称、配色说明或 token 元信息

Technical terms may stay in English when they read better, such as `VNode`, `effect`, `scheduler`, `Fiber`, `queueJob`.

## Working Order

Always follow this order:

1. Classify the type with [diagram-type-matrix.md](references/diagram-type-matrix.md)
2. Extract only the structure that matters for that type
3. Choose `claude-official` unless the user explicitly asks for `default`
4. Start from the matching template in `templates/`
5. Apply [svg-layout-best-practices.md](references/svg-layout-best-practices.md)
6. Apply the matching style reference
7. Validate with `scripts/validate-svg.sh`
8. Render a local preview only when density or branching makes visual review necessary

## Type Selection

Use these rules when the user gives a vague request:

- “系统整体结构 / 模块关系 / 服务依赖 / 部署拓扑” → `architecture`
- “步骤流转 / 决策节点 / 处理流程 / 框架主链路” → `flowchart`
- “数据从哪里来、如何变形、最终写到哪里” → `data-flow`
- “A 调 B，B 再调 C，按时间先后交互” → `sequence`
- “状态变化 / 生命周期 / 事件触发迁移” → `state-machine`
- “路线图 / 阶段推进 / 里程碑” → `timeline`
- “方案对比 / 特性矩阵 / 版本差异” → `comparison-matrix`
- “角色与系统能力关系 / 用例视图” → `use-case`

Framework principle diagrams should usually start from `flowchart` or `data-flow`, not `architecture`.

## Global Rules

- Keep all essential content inside the `viewBox`
- Keep visible safety gaps between regions, nodes, labels, and routed edges
- Use a top note rail for summary notes and a bottom safe rail for legends
- Keep labels on chips or dedicated headers; do not let chips read like floating comments
- For labeled edges, use `edge id + data-edge-id` as the default ownership contract
- Use visible connection ports and keep arrowheads landing on real targets
- Prefer simple shape vocabularies and stronger region boundaries than node borders

Style details live in:

- [style-claude-official.md](references/style-claude-official.md)
- [style-default.md](references/style-default.md)

Layout and semantic contracts live in:

- [svg-layout-best-practices.md](references/svg-layout-best-practices.md)

## Type Rules

### Architecture

- Organize services into 2 to 5 layers and keep cross-layer edges orthogonal

### Flowchart

- Prefer top-to-bottom flow with sparse decisions and branch-owned labels

### Data Flow

- Label major arrows with payloads and keep data/control lanes visually distinct

### Sequence

- Participants sit on the top row
- Messages advance downward in time
- Lifelines stay vertically aligned
- Activation bars show local execution windows
- Keep phase bands inside the time area
- Keep endpoints and activations aligned to lifelines
- For multi-branch frames, use `data-frame-id` and `data-branch`

### State Machine

- Keep initial/final states distinct and put guards on transition labels

### Timeline

- Keep one horizontal time scale and align bars to it

### Comparison Matrix

- Limit columns to a readable count and keep semantic fills consistent

### Use Case

- Keep actors outside the boundary and label `include` / `extend` on dashed relations

## Templates

Use the template that matches the chosen type:

- [architecture.svg](templates/architecture.svg)
- [flowchart.svg](templates/flowchart.svg)
- [data-flow.svg](templates/data-flow.svg)
- [sequence.svg](templates/sequence.svg)
- [state-machine.svg](templates/state-machine.svg)
- [timeline.svg](templates/timeline.svg)
- [comparison-matrix.svg](templates/comparison-matrix.svg)
- [use-case.svg](templates/use-case.svg)

Compatibility templates:

- [assets/template.svg](assets/template.svg) = default `claude-official` starter
- [assets/template-default.svg](assets/template-default.svg) = explicit `default` starter
- [assets/template-claude-official.svg](assets/template-claude-official.svg) = explicit `claude-official` starter

## Validation

Use these local scripts:

- `scripts/validate-svg.sh <svg-file>`
- `scripts/test-templates.sh`

Use `rsvg-convert` only for local verification. The canonical deliverable remains the standalone `.svg`.

## Deliverable Rules

- The final answer should point to the generated `.svg`
- Do not claim success without validation evidence
- Do not generate HTML wrappers by default
- Do not generate PNG by default
- Keep default copy in Chinese
- Keep default style at `claude-official`
- Keep style selection implicit inside the SVG; do not print `claude-official`, `default`, palette notes, or style metadata unless the user explicitly asks for style annotation or comparison
