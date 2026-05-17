---
name: architecture-diagram
description: Use when the user asks for architecture diagrams, technical flowcharts, data-flow diagrams, sequence diagrams, state-machine diagrams, timelines, comparison matrices, use-case diagrams, or framework principle diagrams as standalone SVG deliverables.
---

# Architecture Diagram

Create production-grade technical diagrams as standalone SVG files. Preserve an existing SVG's visual language when revising one; use the style tokens only for new diagrams. Always commit to a structured spec first, render against fixed contracts, then self-review before delivering.

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

Language contract for Chinese output:

- Entity titles must be Chinese-first: write the semantic role in Chinese, then keep necessary English terms, APIs, product names, acronyms, or code identifiers.
- Acceptable: `依赖收集 track`, `模型网关 Model Gateway`, `任务队列 job queue`, `Web 与 REST API`.
- Avoid pure-English entity titles such as `Lifecycle Manager`, `Built-in Tools`, `Renderer Pipeline` unless the entity is a proper noun that has no natural Chinese label.
- Subtitles can be mixed Chinese-English, but they must clarify meaning rather than repeat a pure-English title.

## Working Order

Always follow this order:

1. Classify the type with [diagram-type-matrix.md](references/diagram-type-matrix.md)
2. Clarify only when audience, depth, direction, or whether to split is genuinely unset (see [spec-block-and-self-review.md](references/spec-block-and-self-review.md))
3. If editing an existing SVG, inventory its palette, stroke widths, radius, shadows, typography, and spacing; keep them unless the user asks for a restyle
4. Emit the structured **spec block** before any path; embed it as `<!-- spec ... -->` immediately inside the `<svg>` open tag
5. Choose `claude-official` only for new diagrams unless the user explicitly asks for `default`
6. Start from the matching template in `templates/`
7. Apply [svg-layout-best-practices.md](references/svg-layout-best-practices.md)
8. Apply the matching style reference (typography weights and restyle boundaries are restricted there)
9. Walk the **self-review checklist** in [spec-block-and-self-review.md](references/spec-block-and-self-review.md)
10. Validate with `scripts/validate-svg.sh`
11. Render a local preview when editing an existing SVG or when density / branching makes visual review necessary

Community research and evaluation guidance live in:

- [community-diagram-skill-research.md](references/community-diagram-skill-research.md)
- [generation-eval-set.md](tests/generation-eval-set.md)

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
- For routed architecture edges, add `data-from` and `data-to`; endpoints must land on the source and target borders
- In top-down architecture diagrams, ordinary dependency arrows follow the dominant direction; do not route an edge so the final arrow enters a target from below and points upward unless it is an explicit dashed feedback path
- For one-to-one cross-layer architecture dependencies, align ports and use a straight vertical segment when the horizontal offset is small; do not emit tiny `V-H-V` doglegs
- For one-to-many architecture fan-out with 3 or more destinations, use a labeled bus / hub node; do not stack parallel long `V-H-V` doglegs from the same source port
- Every decision branch must carry `data-edge-label`; never leave a forking edge unlabeled
- Use visible connection ports and keep arrowheads landing on real targets
- Use explicit bus/trunk segments for fan-in or fan-out; bus paths use `edge-bus` and no arrowhead, directed branches use `edge`
- Prefer simple shape vocabularies and stronger region boundaries than node borders
- Do not introduce glassmorphism, neumorphism, gradients, backdrop blur, or new shadow systems when the source SVG already has a working UI style
- Restrict `font-weight` to `400`, `600`, `700`; never emit non-standard values like `740`
- Use `<foreignObject>` with XHTML for paragraphs longer than ~8 CJK characters; never hand-break CJK across multiple `<text>` lines

Style details live in:

- [style-claude-official.md](references/style-claude-official.md)
- [style-default.md](references/style-default.md)

Layout, spec block, and self-review contracts live in:

- [svg-layout-best-practices.md](references/svg-layout-best-practices.md)
- [spec-block-and-self-review.md](references/spec-block-and-self-review.md)

## Type Rules

### Architecture

- Organize services into 2 to 5 layers and keep cross-layer edges orthogonal
- Give every layer region and node body a matching `data-layer-id`
- Use one node body fill per layer; express status or implementation state with badges, stroke, dash, or text, not mixed node backgrounds inside the same layer
- Keep node bodies fully inside their layer region with visible inset on all sides

### Flowchart

- Prefer top-to-bottom flow with sparse decisions and branch-owned labels
- Multi-branch convergence into a shared node uses bus/lane folds, never diagonal entries

### Data Flow

- Label major arrows with payloads via `data-edge-label`
- Keep data and control lanes visually distinct

### Sequence

- Participants sit on the top row
- Messages advance downward in time
- Lifelines stay vertically aligned
- Activation bars show local execution windows
- Keep phase bands inside the time area
- Keep endpoints and activations aligned to lifelines
- For multi-branch frames, use `data-frame-id` and `data-branch`

### State Machine

- Keep initial/final states distinct and put guards on transition labels via `data-guard`

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

- `scripts/validate-svg.sh <svg-file>` for layout / semantic checks
- `scripts/test-templates.sh` for template smoke tests
- `scripts/test-examples.sh` for example SVG regression checks
- `scripts/test-generated-complex.sh` for complex generated diagram checks
- `scripts/test-generated-stress.sh` for high-density stress diagram checks
- `scripts/test-semantic-negative.sh` for validator regression checks that must fail malformed SVGs
- `scripts/test-all.sh` for the full local validation suite

Use `rsvg-convert` only for local verification. The canonical deliverable remains the standalone `.svg`.

## Deliverable Rules

- The final answer should point to the generated `.svg`
- Do not claim success without validation evidence
- Do not generate HTML wrappers by default
- Do not generate PNG by default
- Keep default copy in Chinese
- Keep default style at `claude-official`
- Keep style selection implicit inside the SVG; do not print `claude-official`, `default`, palette notes, or style metadata unless the user explicitly asks for style annotation or comparison
- If self-review flags a failure, fix in place and state which items now pass before delivering
