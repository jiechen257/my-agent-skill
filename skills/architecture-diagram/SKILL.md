---
name: architecture-diagram
description: Use when the user asks for architecture diagrams, technical flowcharts, data-flow diagrams, sequence diagrams, state-machine diagrams, timelines, comparison matrices, use-case diagrams, or framework principle diagrams as standalone SVG deliverables.
---

# Architecture Diagram

Create production-grade technical diagrams as standalone SVG files.

## Scope

This skill covers a **standard refactor** subset of the broader `fireworks-tech-graph` idea:

- `architecture`
- `flowchart`
- `data-flow`
- `sequence`
- `state-machine`
- `timeline`
- `comparison-matrix`
- `use-case`

This skill intentionally supports only two visual styles:

- `claude-official`
- `default`

## Output Defaults

- 默认输出语言：中文
- 默认风格：`claude-official`
- 默认主题：light
- 默认交付物：单个 `.svg`
- 默认不生成 `.html`
- 默认不生成 `.png`

Technical terms may stay in English when they read better, such as `VNode`, `effect`, `scheduler`, `Fiber`, `queueJob`.

## Working Order

Always follow this order:

1. **Classify the diagram type** using [diagram-type-matrix.md](references/diagram-type-matrix.md)
2. **Extract the structure**:
   - architecture: layers, services, stores, external systems
   - flowchart: start, process, decision, I/O, end
   - data-flow: producers, transforms, stores, consumers, payload labels
   - sequence: participants, messages, frames, activation windows
   - state-machine: states, transitions, guards, initial/final nodes
   - timeline: phases, durations, milestones, dependencies
   - comparison-matrix: columns, rows, criteria, cell semantics
   - use-case: actors, system boundary, use cases, include/extend relations
3. **Choose the style**:
   - use `claude-official` unless the user explicitly asks for `default`
4. **Start from the matching template** in `templates/`
5. **Apply layout rules** from [svg-layout-best-practices.md](references/svg-layout-best-practices.md)
6. **Apply style tokens** from:
   - [style-claude-official.md](references/style-claude-official.md)
   - [style-default.md](references/style-default.md)
7. **Validate the SVG** with `scripts/validate-svg.sh`
8. **Optionally render a local preview** for verification only

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

## Style System

### `claude-official`

Use this when the prompt does not specify a style.

Characteristics:

- warm cream page background
- darker gray outline system
- soft muted fills
- thicker strokes
- softer shadows
- restrained connector colors
- stronger editorial-card feeling

This style works well for:

- framework principle diagrams
- architecture overviews
- documentation-ready diagrams
- comparison matrices
- timelines

### `default`

Use this only when the user explicitly asks for:

- `default`
- 彩色分区
- 更强语义色
- 流程阶段配色

Characteristics:

- neutral light canvas
- semantic phase colors
- clearer category-coded arrows
- stronger region tint differences
- more visible flow segmentation

## Shared Layout Rules

All diagram types must obey these base rules:

- Keep all essential content inside the `viewBox`
- Use a top note rail for summary notes; never float long note cards inside the routing core
- Keep note cards fully inside the inner frame; keep at least 40px right inset and expand leftward before text overflows
- Keep legend content inside a bottom safe rail; keep at least 56px bottom inset and wrap to two rows when one row is too wide
- Keep labels on opaque chips or dedicated header areas
- Use visible connection ports; arrowheads must land on node edges, lifelines, state borders, or matrix cells
- Keep competing lines on separate corridors
- Avoid unrelated edge overlap on the same corridor segment
- Reserve one extra lane for feedback or return flow
- Use a small shape vocabulary with visible semantic differences
- Keep region boundaries stronger than node borders

## Shape Vocabulary

Use only the shapes needed by the chosen type.

- **Phase band**: top-level section container
- **Title pill**: section title chip
- **Standard node**: normal processing box
- **Terminal node**: input, output, external endpoint, or final result
- **Decision node**: diamond for explicit branch points
- **I/O node**: slanted parallelogram for request/response or file input/output
- **Subpanel**: local sub-flow or explanatory inset
- **Label chip**: arrow label, lane label, merge label
- **Note card**: note rail callout
- **Lifeline**: sequence participant vertical guide
- **Activation bar**: active execution window on a lifeline
- **State node**: rounded state block
- **Milestone marker**: diamond or circle on a timeline
- **Matrix cell**: comparison table cell with semantic fill
- **Use-case ellipse**: capability inside a system boundary

## Type Rules

### Architecture

- Organize services into 2 to 5 layers
- Keep cross-layer edges orthogonal
- Use phase bands or dashed grouping containers
- Put stores and external systems on visually distinct shapes

### Flowchart

- Prefer top-to-bottom flow
- Use `terminal -> process -> decision -> process -> end`
- Keep decisions sparse and explicit
- Split branch labels onto dedicated chips

### Data Flow

- Label every major arrow with the payload
- Use wider primary paths for the main data stream
- Separate control flow from data flow
- Keep transforms and stores visually distinct

### Sequence

- Participants sit on the top row
- Messages advance downward in time
- Lifelines stay vertically aligned
- Activation bars show local execution windows

### State Machine

- Initial and final nodes must be visually distinct
- Guards belong on transition labels
- Keep main loop readable before adding side transitions

### Timeline

- Time axis stays horizontal
- Bars align to one scale
- Milestones sit above or below the axis with clear labels

### Comparison Matrix

- Limit columns to a readable count
- Use alternating row fills
- Use semantic fills for `支持 / 部分支持 / 不支持`

### Use Case

- Actors stay outside the system boundary
- Use cases stay inside the boundary
- `include` and `extend` must be labeled on dashed relations

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

## Validation

Use these local scripts:

- `scripts/validate-svg.sh <svg-file>`
- `scripts/test-templates.sh`

Use `rsvg-convert` for local verification only. The canonical deliverable remains the standalone `.svg`.

## Deliverable Rules

- The final answer should point to the generated `.svg`
- Do not claim success without validation evidence
- Do not generate HTML wrappers by default
- Do not generate PNG by default
- Keep default copy in Chinese
- Keep default style at `claude-official`
