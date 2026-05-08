# Diagram Type Matrix

Use this matrix before drawing.

| User Intent | Diagram Type | Backbone | Primary Shapes |
|---|---|---|---|
| 系统模块、服务边界、上下游关系 | `architecture` | horizontal layers | phase band, standard node, terminal node, subpanel |
| 步骤流转、条件分支、框架主链路 | `flowchart` | top-to-bottom process chain | terminal, process, decision, I/O |
| 数据如何产生、变换、存储、回传 | `data-flow` | source → transform → store → consumer | source node, transform node, store node, label chip |
| 调用时序、消息交换、参与者交互 | `sequence` | participant columns + time axis downward | lifeline, activation bar, message arrow, frame |
| 生命周期、状态迁移、守卫条件 | `state-machine` | state graph with readable main loop | initial node, state node, choice, final node |
| 阶段推进、里程碑、排期 | `timeline` | horizontal time axis | phase bar, milestone, dependency line |
| 方案对比、特性矩阵、版本比较 | `comparison-matrix` | table grid | header cell, row header, semantic cell |
| 角色与能力关系、系统用例边界 | `use-case` | system boundary + actors outside | actor, use-case ellipse, boundary rect |

## Selection Rules

- Choose the type that preserves the user’s mental model with the fewest visual conversions.
- Prefer `flowchart` over `architecture` for framework runtime loops and compile/runtime/update chains.
- Prefer `data-flow` over `flowchart` when payload labels matter more than decision logic.
- Prefer `sequence` when the order of calls matters more than component grouping.
- Prefer `comparison-matrix` when the user asks “差异、对比、优缺点、支持情况”.
- Prefer `timeline` when dates or relative phases are part of the story.

## Default Style Mapping

- Use `claude-official` by default for every type.
- Use `default` only when the user explicitly asks for stronger semantic color separation.
