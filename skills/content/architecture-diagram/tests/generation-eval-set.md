# Architecture Diagram Generation Eval Set

Use this set to evaluate whether `architecture-diagram` can generate polished standalone SVGs across supported diagram types.

## Run Protocol

For each case:

1. Generate one standalone `.svg` from the prompt.
2. Keep the default language Chinese and the default style `claude-official`.
3. Run `scripts/validate-svg.sh <generated.svg>`.
4. Render a local preview for visual review when the diagram has branches, cross-layer routing, frames, or dense labels.
5. Score the case against the acceptance probes below.

Scoring:

- `2`: passes validator and all visual probes
- `1`: passes validator with minor visual issues
- `0`: fails validation, clips content, overlaps UI, or misrepresents the requested structure

## Case 1: Flowchart Branch Merge

Prompt:

```text
画一个退款审批流程图：用户提交退款申请，系统校验订单状态，若符合条件则自动退款并通知用户，若不符合条件则进入人工复核，复核通过后退款，复核拒绝后通知拒绝原因。突出决策分支和最终输出。
```

Expected type: `flowchart`

Acceptance probes:

- Decision branch labels sit on branch-owned segments.
- Every arrowhead lands on a process, decision, I/O, terminal, or explicit merge target.
- Branch convergence uses orthogonal folds or a bus; no arrow floats in whitespace.
- No branch line crosses through the decision diamond or output node text.

## Case 2: Layered Architecture

Prompt:

```text
画一个订单系统架构图：入口层包含 Web/App、API Gateway；处理层包含订单服务、支付服务、库存服务、消息队列；数据层包含订单库、库存库、缓存。请求从入口进入订单服务，订单服务同步调用库存服务和支付服务，并异步写入消息队列，最终更新订单库和缓存。
```

Expected type: `architecture`

Acceptance probes:

- 2 to 5 layers have clear region boundaries and visible insets.
- Cross-layer edges route through corridors and avoid sitting on region borders.
- Architecture edges use border-to-border endpoints and declare stable ownership where applicable.
- Nodes inside one layer keep a coherent fill strategy; status is expressed with text, badge, stroke, or dash.

## Case 3: Comparison Matrix

Prompt:

```text
画一个技术方案对比矩阵：方案 A 是直接重写，方案 B 是渐进迁移，方案 C 是旁路新系统。维度包括复杂度、上线风险、可维护性、交付周期、团队学习成本。用低/中/高表达每格结论。
```

Expected type: `comparison-matrix`

Acceptance probes:

- Matrix has a top-left header cell such as `评估维度`.
- Header row is visually stronger than body rows.
- Row labels and cell values stay centered inside cells.
- Semantic fills stay consistent for low, medium, and high values.

## Case 4: Data Flow With Feedback

Prompt:

```text
画一个日志数据流图：客户端事件进入采集网关，经过清洗、脱敏、聚合，写入明细存储和指标存储，再被监控看板和告警系统消费。告警系统会把异常规则回写到清洗阶段。
```

Expected type: `data-flow`

Acceptance probes:

- Every major arrow has a payload label on an opaque chip.
- Data flow and feedback/control flow use separate lanes.
- Feedback edge starts from the producing entity border and ends on the consuming entity border.
- Stores and transforms use distinct shape or fill semantics.

## Case 5: Sequence With Alternate Branches

Prompt:

```text
画一个支付确认时序图：前端调用订单服务，订单服务调用支付服务创建支付单，支付服务回调订单服务。回调成功时订单服务通知履约服务；回调失败时订单服务通知用户并关闭订单。需要展示 alt 分支和激活条。
```

Expected type: `sequence`

Acceptance probes:

- Participants align to lifelines.
- Messages advance downward in time and stay horizontal.
- Activation bars overlap message endpoints.
- `alt` frame encloses both branch messages; branch 1 stays above separator, branch 2 stays below separator.

## Case 6: State Machine With Retry

Prompt:

```text
画一个任务状态机：初始进入待调度，submit 后进入执行中，成功后进入已完成，失败且可重试时进入等待重试，重试次数耗尽后进入已失败，取消事件可从待调度或执行中进入已取消。标出 guard 条件。
```

Expected type: `state-machine`

Acceptance probes:

- Initial and final states are visually distinct.
- Guards appear on transition labels.
- Retry loop is readable and uses an outer lane.
- Transition endpoints land on state borders.

## Case 7: Timeline Roadmap

Prompt:

```text
画一个 2026 年路线图时间线：Q1 完成调研和范围收敛，Q2 完成核心实现，Q3 完成灰度和性能优化，Q4 完成正式发布和复盘。标出两个里程碑：MVP 评审、正式发布。
```

Expected type: `timeline`

Acceptance probes:

- One horizontal time scale drives all bars.
- Bars align to the same scale and do not overlap labels.
- Milestone markers sit above or below the axis with readable labels.
- Bottom and right safe insets remain visible.

## Case 8: Use Case Relations

Prompt:

```text
画一个内容发布系统用例图：作者可以创建草稿、提交审核、查看发布结果；审核员可以审核内容；管理员可以配置发布规则。提交审核 include 内容校验，创建草稿 extend 补充素材。角色必须在系统边界外。
```

Expected type: `use-case`

Acceptance probes:

- Actors stay outside the system boundary.
- Use cases stay inside the boundary.
- `include` and `extend` use dashed labeled relations.
- Relation endpoints land on use-case ellipse borders.

## Case 9: Split-Diagram Decision

Prompt:

```text
同时画出 AI 代码助手的系统架构、用户请求处理流程、工具调用时序、任务状态流转和能力对比表，要求一张图里全部讲清楚。
```

Expected behavior: ask to split or emit a plan for multiple SVGs.

Acceptance probes:

- The skill identifies mixed diagram types.
- The skill proposes an overview plus focused sub-diagrams.
- It avoids placing architecture, flowchart, sequence, state machine, and matrix content into one overloaded SVG.
