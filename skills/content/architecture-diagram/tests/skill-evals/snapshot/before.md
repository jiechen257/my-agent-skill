Use when the user asks for architecture diagrams, technical flowcharts, data-flow diagrams, sequence diagrams, state-machine diagrams, timelines, comparison matrices, use-case diagrams, or framework principle diagrams as standalone SVG deliverables.

# Architecture Diagram

Create production-grade technical diagrams as standalone SVG files.

Supported types: `architecture`, `flowchart`, `data-flow`, `sequence`, `state-machine`, `timeline`, `comparison-matrix`, `use-case`

## Output Defaults

- 默认输出语言：中文
- 默认主题：light
- 默认交付物：单个 `.svg`
- Technical terms may stay in English when they read better

## Working Order

1. Classify the diagram type
2. Extract only the structure that matters
3. Build the SVG with proper layout
4. Validate completeness

## Type Selection

- "系统整体结构 / 模块关系 / 服务依赖 / 部署拓扑" → `architecture`
- "步骤流转 / 决策节点 / 处理流程 / 框架主链路" → `flowchart`
- "数据从哪里来、如何变形、最终写到哪里" → `data-flow`
- "A 调 B，B 再调 C，按时间先后交互" → `sequence`
- "状态变化 / 生命周期 / 事件触发迁移" → `state-machine`
- "路线图 / 阶段推进 / 里程碑" → `timeline`
- "方案对比 / 特性矩阵 / 版本差异" → `comparison-matrix`
- "角色与系统能力关系 / 用例视图" → `use-case`

## Global Rules

- Keep all essential content inside the `viewBox`
- Keep visible safety gaps between regions, nodes, labels, and routed edges
- Use a top note rail for summary notes and a bottom safe rail for legends
- For labeled edges, use `edge id + data-edge-id` as the default ownership contract
- Use visible connection ports and keep arrowheads landing on real targets
- Prefer simple shape vocabularies and stronger region boundaries than node borders

## Type-specific Rules

- **Architecture**: 2-5 layers, orthogonal cross-layer edges
- **Flowchart**: top-to-bottom, sparse decisions, branch-owned labels
- **Data Flow**: label major arrows with payloads, distinct data/control lanes
- **Sequence**: participants top row, messages advance downward, lifelines aligned
- **State Machine**: distinct initial/final states, guards on transition labels
- **Timeline**: one horizontal time scale, bars aligned
- **Comparison Matrix**: readable column count, consistent semantic fills
- **Use Case**: actors outside boundary, label include/extend on dashed relations

## Deliverable Rules

- The final answer should point to the generated `.svg`
- Do not generate HTML wrappers or PNG by default
- Keep default copy in Chinese
