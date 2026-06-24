# Skill 使用手册与白皮书

更新时间：2026-06-24
适用仓库：`/Users/zhici/work-pro/my-agent-skill`

## 1. 定位

本仓库集中维护个人 Codex / Claude Code skills。`skills/` 下的每个 `SKILL.md` 都是会被安装和自动发现的 active 入口；`vendor/skills/` 保存外部同步源快照，供 wrapper 按需读取。

截至本文档更新时，`skills/` 下有 33 个 active `SKILL.md`，`vendor/skills/` 下有 26 个上游 source `SKILL.md`。真实安装面固定为 active wrapper；Trellis / Waza / Superpowers 的冲突由 `rules/codex-global.md` 和 `skills/workflow/*` router 在运行时裁决。

| 类别 | 数量 | 说明 |
| --- | ---: | --- |
| `design` | 2 | 本地设计辅助和 Waza design wrapper |
| `workflow` | 5 | Trellis 深度规划、Waza workflow router、grill-me wrapper |
| `harness` | 2 | MCP 健康检查和 Waza health wrapper |
| `research-docs` | 9 | 周报、技术选型、会话交接、Waza 研究读写、leonsong09 日报/笔记 wrapper |
| `hone` | 1 | frontier AI coding signals 与本地 agent harness 实践 |
| `superpowers` | 14 | 显式点名才使用的 Superpowers wrapper |

`registry/skills.yaml` 同时登记 active wrapper 和 vendored source snapshot。`install.sh` 只安装 `codex: true` / `claude: true` 的 active wrapper；`codex: false` 且 `claude: false` 的 source snapshot 只供 `scripts/sync-vendored-skills.sh` 更新。

workflow owner 的选择规则：

| 项目上下文 | workflow owner | 关键效果 |
| --- | --- | --- |
| 存在 `.trellis/workflow.md` | Trellis | `think` / `check` / `hunt` wrapper 只做路由，不启动 Waza 或 Superpowers workflow |
| 不存在 `.trellis/workflow.md` | Waza | `think` / `check` / `hunt` wrapper 读取 `vendor/skills/waza/*` 并执行 |
| 用户显式点名 Superpowers skill | Superpowers explicit wrapper | 只在明确点名时读取对应 `vendor/skills/superpowers/superpowers/*` |

## 2. 使用总原则

先判断任务类型，再选择 skill。简单任务不需要堆流程；高风险任务、返工、bug、跨模块改动必须先收集证据再行动。

使用 skill 时遵守以下顺序：

1. 确认用户请求是否显式点名 skill。
2. 若未点名，按场景匹配最接近的 skill。
3. 读取对应 `SKILL.md` 的完整内容，再执行。
4. 如果 skill 引用 `references/`、`scripts/`、`agents/`、`assets/`，只读取或运行当前任务必需的部分。
5. 修改文件前说明将改什么；修改后运行与风险匹配的验证。
6. 不还原用户已有改动；脏工作区只处理当前任务相关文件。

不要同时启动两套完整流程。比如一个 bug 修复不要同时走 `hunt`、`systematic-debugging`、`think` 三条主流程；选一个 workflow owner，其他 skill 只作为原子方法参考。

## 3. 场景速查

| 用户意图或场景 | 首选 skill | 可组合 skill | 注意事项 |
| --- | --- | --- | --- |
| 做一个新功能、交互、组件或行为变化 | `think` | `grill-me` | 需求不清时先收敛目标、影响面、验收方式。 |
| 用户要求“出方案”“怎么设计”“有没有必要” | `think` | `grill-me` | 输出决策完整的方案，不直接写代码。 |
| 用户要被追问、压测方案 | `grill-me` | `think` | 一次问一个问题；能从代码查到的就先查。 |
| bug、异常、构建失败、测试失败 | `hunt` | `check` | 先复现、追数据流、提出假设，再修复。 |
| 代码审查、合并前检查、发布前检查 | `check` | `hunt` | findings 先行，按严重程度排序。 |
| UI 设计、页面打磨、截图复刻 | `design` | `colawd-ui-style` | 先确认产品语境和现有风格，不做泛化模板页。 |
| 复刻 colawd 风格工作台 | `colawd-ui-style` | `design` | 保持黑色 shell、浅黄网格、粗边框、硬阴影等风格约束。 |
| MCP 配置异常 | `mcp-healthcheck` | `health` | 以当前机器证据为准，先诊断再改配置。 |
| 今天做了什么、提交日报 | `commit-daily-summary` | `project-daily-summary` | commit 证据优先，不用记忆替代 git。 |
| 按项目总结今天所有 Codex 工作 | `project-daily-summary` | `commit-daily-summary` | 同时看会话、提交和未提交变更。 |
| 周报 | `weekly-report-template` | `commit-daily-summary` | 只覆盖用户指定 repo 和时间段。 |
| 读链接、读 PDF、转 Markdown | `read` | `research-note-wrap` | 外部最新信息要实时验证并保留来源。 |
| 深入研究、整合资料成文章 | `learn` | `tech-solution-radar`、`write` | 适合多来源，不适合单个快速查找。 |
| 技术选型、工具对比、最佳实践调研 | `tech-solution-radar` | `read`、`research-note-wrap` | 给证据、评分和推荐，不只罗列优缺点。 |
| 润色、改稿、去 AI 味 | `write` | `read` | 保留原意，不虚构事实。 |
| 总结调研为 Obsidian 笔记 | `research-note-wrap` | `learn` | 明确输出位置和范围。 |
| 写交接 prompt 给另一个 agent | `session-handoff` | `project-daily-summary` | 生成自包含交接文件，不泄露密钥。 |
| frontier AI coding / hone 相关讨论 | `hone` | `health` | 聚焦 signals、harness drift 和本地实践映射。 |
| 创建或修改 skill | `hone` | `check` | skill 本身也要有触发场景、流程和验证方式。 |

## 4. 核心 active skills

### 4.1 `design`

路径：`skills/design/design/SKILL.md`

适用场景：

- 用户要求做页面、组件、UI、前端、视觉界面。
- 用户说页面丑、不清楚、不一致、截图不对。
- 需要从截图或已有产品风格推导可执行的 UI 改造。

典型 case：

- 把一个数据后台页面改得更像真实工作台。
- 根据截图修复字号、间距、层级、空状态、hover、响应式。
- 给页面建立稳定视觉方向，而不是套用默认卡片模板。

注意事项：

- 不是后端逻辑或数据管线 skill。
- 先看现有 repo 和设计上下文；已有产品不应被无关地整体重皮。
- 前端完成后尽量启动本地服务并截图或浏览器验证。

### 4.2 `colawd-ui-style`

路径：`skills/design/colawd-ui-style/SKILL.md`

适用场景：

- 用户明确要求 colawd 风格。
- 需要复刻黑色 terminal shell、浅黄网格 canvas、粗黑边框、硬阴影、霓虹状态色、双语生产力 UI。

典型 case：

- 做 colawd 风格 dashboard、library、capture、create、publish 工作流。
- 审查页面是否符合 colawd 截图里的视觉 token 和组件语法。

注意事项：

- 这是强风格 skill，不适合所有 UI。
- 使用时要检查视觉 token、sidebar、header controls、cards、buttons、data visualization 是否一致。

### 4.3 `think`

路径：`skills/workflow/think/SKILL.md`

适用场景：

- 用户问“出方案”“怎么设计”“有没有必要”“值不值得”“plan this”。
- 功能、架构、价值判断需要先收敛决策，再进入实现。

典型 case：

- 新功能设计前比较 2 到 3 个实现方向。
- 判断一个复杂抽象是否值得引入。
- 把粗糙想法变成可批准、可移交的计划。

注意事项：

- 不用于 bug 修复或很小的直接编辑。
- 输出要包含推荐方案、取舍、验证方式和实现交接边界。

### 4.4 `grill-me`

路径：`skills/workflow/grill-me/SKILL.md`

适用场景：

- 用户要求“grill me”或希望被追问、压测方案。
- 计划里有多个依赖决策，需要逐分支澄清。

典型 case：

- 在正式实施前审问产品方案的目标、约束、风险、替代方案。
- 对架构计划逐层追问，直到双方理解一致。

注意事项：

- 一次只问一个问题。
- 如果问题可以通过读代码回答，就先读代码，不把问题丢回用户。
- 每个问题都应给出推荐答案，帮助用户决策。

### 4.5 `check`

路径：`skills/workflow/check/SKILL.md`

适用场景：

- review diff、PR、issue 队列、release readiness、commit、push、publish。
- 用户说“看看代码”“合并前看下”“review 一下”“能不能发版”。

典型 case：

- 本地改动提交前审查。
- PR review findings 输出。
- 发布前检查风险和缺失验证。
- 执行已批准计划并在安全门后推进。

注意事项：

- 默认 review 立场：先列问题和风险，再给摘要。
- 不是根因调试入口；bug 应走 `hunt` 或 `systematic-debugging`。
- 遇到 dirty worktree 要先识别哪些改动属于当前任务。

### 4.6 `hunt`

路径：`skills/workflow/hunt/SKILL.md`

适用场景：

- 排查报错、崩溃、回归、测试失败、截图缺陷、之前能用现在不能用。
- 用户明确要判断为什么失败。

典型 case：

- 前端状态和后端数据不一致。
- 构建失败但错误堆栈很长。
- 上轮修复后问题再次出现，需要 break loop。

注意事项：

- 先诊断后修复；必须有证据链、假设、最小验证。
- 不要在症状点直接补丁。
- 多组件问题先确认问题发生在哪一层。

### 4.9 `mcp-healthcheck`

路径：`skills/harness/mcp-healthcheck/SKILL.md`

适用场景：

- 检查 Codex MCP servers 可达性、认证类型、代理行为、命令可用性、tool-list drift、写工具风险。

典型 case：

- MCP 工具消失或调用失败。
- 代理/no-proxy 导致 MCP 连接异常。
- 需要确认某个 server 是否具备写权限。

注意事项：

- 区分 reachability、auth、工具注册和运行时权限。
- 输出要包含验证命令和结果。

### 4.10 `health`

路径：`skills/harness/health/SKILL.md`

适用场景：

- 用户要求检查 Claude/Codex/PI 配置、健康度、agent 是否忽略指令、验证面缺失、代码 AI 可维护性下降。

典型 case：

- 审计 instruction/config drift。
- 检查 hooks、MCP、verifier surfaces。
- 给项目按 tier 输出工程健康报告。

注意事项：

- 这是工程健康审计，不是具体 bug 修复。
- 报告要分 PASS、finding、风险和可执行建议。

### 4.12 `hone`

路径：`skills/hone/SKILL.md`

适用场景：

- 用户提到 hone。
- 讨论 frontier AI coding signals、本地 agent harness、Codex skills/rules/hooks/MCP config、Codex/Claude harness drift。

典型 case：

- 把外部 agent coding trend 映射到本地 skill/harness 改造。
- 判断某个 harness 信号是否值得沉淀。

注意事项：

- 避免泛泛趋势复述；要落到本地状态模型、写入边界和完成契约。

### 4.13 `commit-daily-summary`

路径：`skills/research-docs/commit-daily-summary/SKILL.md`

适用场景：

- 用户问今天提交了什么、今天做了什么、提交总结、日报。

典型 case：

- 从某个 repo 当天 git commits 生成中文日报。
- 按 workstream 分组重写成行动摘要。

注意事项：

- commit 证据优先。
- 不要把未提交工作和 commit-based summary 混为一谈，除非用户要求。

### 4.14 `project-daily-summary`

路径：`skills/research-docs/project-daily-summary/SKILL.md`

适用场景：

- 用户要按项目总结今天所有 Codex 工作，合并会话、计划、完成项、提交和未提交变更。

典型 case：

- 生成一天跨多个 repo 的项目日报。
- 从 Codex session transcript 提取项目活动。

注意事项：

- 使用本地日期。
- 子 agent 活动要归到正确项目，不应重复计数。

### 4.15 `weekly-report-template`

路径：`skills/research-docs/weekly-report-template/SKILL.md`

适用场景：

- 用户要求周报、周进展、指定 repo 和指定周的总结。

典型 case：

- 按固定四段式模板生成周报。
- 合并 git commits 与用户批准的补充材料。

注意事项：

- 必须明确时间范围和 repo scope。
- 不覆盖未指定仓库。

### 4.16 `research-note-wrap`

路径：`skills/research-docs/research-note-wrap/SKILL.md`

适用场景：

- 用户要把调研、分析、会话结论整理成可读 Obsidian Markdown 笔记。

典型 case：

- 把当前会话的方案讨论整理为研究笔记。
- 按主题汇总今天多个会话的结论。

注意事项：

- 先决定 scope：当前会话还是跨会话。
- 先决定输出位置，避免把临时分析文档写进源码目录。

### 4.18 `tech-solution-radar`

路径：`skills/research-docs/tech-solution-radar/SKILL.md`

适用场景：

- 调研社区或行业最佳实践、开源替代、库、框架、SaaS、架构模式、技术方案。

典型 case：

- 比较多个工具并按功能匹配、流行度、维护状态打分。
- 输出推荐结论、排名表、证据表和选择建议。

注意事项：

- 外部事实可能变化，必须实时验证。
- 不只给主观看法，要给来源和评分依据。

### 4.19 `session-handoff`

路径：`skills/research-docs/session-handoff/SKILL.md`

适用场景：

- 用户要写 prompt 给另一个 agent、交接给同事或新的 Codex/Claude session。

典型 case：

- 当前任务未完成，需要冷启动另一个 agent 接手。
- 把当前环境、进度、关键文件、验证方法和开放问题打包成自包含交接文档。

注意事项：

- 输出是交接 artifact，不是普通聊天摘要。
- 必须包含环境、当前任务、历史、下一步、关键文件、验证方法、开放决策。
- 不泄露 `.env`、token、API key、DSN。

### 4.21 `learn`

路径：`skills/research-docs/learn/SKILL.md`

适用场景：

- 深入研究陌生领域、整理大量材料、把来源转成可发布文章或 coherent reference。

典型 case：

- 从多篇文章和链接整理一篇技术综述。
- 把原始材料变成结构化长文。

注意事项：

- 不适合快速单链接读取。
- 按 collect、digest、outline、fill in、refine、self-review 推进。

### 4.22 `read`

路径：`skills/research-docs/read/SKILL.md`

适用场景：

- 读取 URL 或 PDF，做简短总结、Markdown 转换、引用摘录、保存给下游任务。

典型 case：

- “看这个链接”。
- “把这个 PDF 转成 Markdown”。
- 从网页提取内容给后续设计或调研使用。

注意事项：

- 不用于 repo 内本地文本文件。
- 要遵守版权和引用限制。
- 私密或登录态内容要区分 fetch tier。

### 4.23 `write`

路径：`skills/research-docs/write/SKILL.md`

适用场景：

- 中文或英文文稿润色、去 AI 味、改稿、审稿、release notes、social posts。

典型 case：

- 把 AI 味很重的段落改自然。
- 改 GitHub issue 回复或发布说明。

注意事项：

- 保留原意和事实边界。
- 不用于代码注释、commit message 或 inline docs 的机械生成。

## 5. Explicit Superpowers wrappers

这些 active wrapper 位于 `skills/superpowers/`，只在用户显式点名对应 Superpowers skill 时触发。wrapper 会读取 `vendor/skills/superpowers/superpowers/` 下的上游源；不要在本仓库手动修改 vendored 源内容。

### 5.1 `using-superpowers`

路径：`skills/superpowers/using-superpowers/SKILL.md`

适用场景：

- 用户明确点名 `using-superpowers`。
- 临时希望采用完整 Superpowers skill 路由自检。

注意事项：

- 它强调先查 skill 再行动。
- 不作为全局默认入口；在 Trellis 项目中尤其不能覆盖 Trellis workflow owner。
- 若与用户明确规则或上层系统规则冲突，以上层规则为准。

### 5.2 `brainstorming`

路径：`skills/superpowers/brainstorming/SKILL.md`

适用场景：

- 用户明确点名 `brainstorming` 或 `$brainstorming`。
- 临时希望使用 Superpowers 的需求澄清和设计 approval gate。

典型 case：

- 从模糊 idea 收敛出设计。
- 提供 2 到 3 个方案并选择推荐方向。

注意事项：

- 原 skill 有严格 approval gate；在本仓库使用时要同时遵守用户全局 AGENTS 的任务分流规则。
- 对轻量任务可以保留“先看上下文、明确 DoD”的核心，不应机械扩大流程。

### 5.3 `writing-plans`

路径：`skills/superpowers/writing-plans/SKILL.md`

适用场景：

- 用户明确点名 `writing-plans`。
- 已有 spec 或明确需求，需要临时使用 Superpowers 的多步骤实施计划格式。

典型 case：

- 把批准的方案拆成 bite-sized implementation tasks。
- 为另一个 agent 写可执行计划。

注意事项：

- 不要写占位符。
- 计划要包含文件、改动、测试和交接说明。

### 5.4 `executing-plans`

路径：`skills/superpowers/executing-plans/SKILL.md`

适用场景：

- 用户明确点名 `executing-plans`。
- 已有书面计划，需要临时使用 Superpowers 的计划执行纪律。

典型 case：

- 在独立 session 中执行 implementation plan。
- 执行过程中发现计划过期，需要回到早期步骤。

注意事项：

- 先加载并审查计划。
- 遇到阻塞要停下来说明，不要静默改计划。

### 5.5 `test-driven-development`

路径：`skills/superpowers/test-driven-development/SKILL.md`

适用场景：

- 用户明确点名 `test-driven-development`。
- 希望临时使用 Superpowers 的严格 TDD discipline。

典型 case：

- 为回归 bug 写失败用例。
- 为纯函数、边界条件、关键业务逻辑加测试。

注意事项：

- 遵守 red、green、refactor 顺序。
- 如果无法写测试，要说明原因并给替代验证。

### 5.6 `systematic-debugging`

路径：`skills/superpowers/systematic-debugging/SKILL.md`

适用场景：

- 用户明确点名 `systematic-debugging`。
- 希望临时使用 Superpowers 的系统化调试 discipline。

典型 case：

- 先找 root cause，再修复。
- 验证假设后实施最小改动。

注意事项：

- 四阶段：root cause investigation、pattern analysis、hypothesis and testing、implementation。
- 不允许“看起来像”就修。

### 5.7 `verification-before-completion`

路径：`skills/superpowers/verification-before-completion/SKILL.md`

适用场景：

- 用户明确点名 `verification-before-completion`。
- 希望临时使用 Superpowers 的完成前验证 checklist。

典型 case：

- 最后跑 lint、typecheck、unit test、build。
- 前端任务做浏览器或截图验证。

注意事项：

- 证据先于结论。
- 如果验证失败或无法运行，必须明确说明。

### 5.8 `requesting-code-review`

路径：`skills/superpowers/requesting-code-review/SKILL.md`

适用场景：

- 用户明确点名 `requesting-code-review`。
- 希望临时使用 Superpowers 的 review 请求格式。

典型 case：

- 把变更摘要、测试结果、风险点交给 reviewer。

注意事项：

- 不要在明显缺少验证时请求 review。

### 5.9 `receiving-code-review`

路径：`skills/superpowers/receiving-code-review/SKILL.md`

适用场景：

- 用户明确点名 `receiving-code-review`。
- 希望临时使用 Superpowers 的 review feedback 处理纪律。

典型 case：

- 判断反馈是否正确、是否值得做、是否需要反驳。
- 对不清晰反馈做 technical clarification。

注意事项：

- 不盲目接受。
- 不用“professional-looking”改动扩大范围。

### 5.10 `dispatching-parallel-agents`

路径：`skills/superpowers/dispatching-parallel-agents/SKILL.md`

适用场景：

- 用户明确点名 `dispatching-parallel-agents`。
- 希望临时使用 Superpowers 的并行分派纪律。

典型 case：

- 一个 agent 查 API，一个 agent 查 UI，一个 agent 查测试。
- 多 repo 独立扫描。

注意事项：

- 子任务必须边界清楚、无共享写状态。
- 主 agent 负责整合和冲突处理。

### 5.11 `subagent-driven-development`

路径：`skills/superpowers/subagent-driven-development/SKILL.md`

适用场景：

- 用户明确点名 `subagent-driven-development`。
- 希望临时使用 Superpowers 的子 agent 开发纪律。

典型 case：

- 拆分实现、测试、文档子任务。

注意事项：

- 不适合高度耦合或需要连续上下文的改动。
- 子 agent 结果必须由主 agent 审核。

### 5.12 `using-git-worktrees`

路径：`skills/superpowers/using-git-worktrees/SKILL.md`

适用场景：

- 用户明确点名 `using-git-worktrees`。
- 希望临时使用 Superpowers 的 worktree 隔离流程。

典型 case：

- 当前 worktree 有用户未提交改动，不能直接改。
- 多个 feature 并行。

注意事项：

- 先检测是否已有隔离环境。
- 使用 native worktree tools 或 git worktree fallback。

### 5.13 `finishing-a-development-branch`

路径：`skills/superpowers/finishing-a-development-branch/SKILL.md`

适用场景：

- 用户明确点名 `finishing-a-development-branch`。
- 希望临时使用 Superpowers 的分支收尾流程。

典型 case：

- 分支收尾时给用户结构化选项。

注意事项：

- 先验证测试，再判断 base branch 和集成路径。
- 不要擅自做破坏性 cleanup。

### 5.14 `writing-skills`

路径：`skills/superpowers/writing-skills/SKILL.md`

适用场景：

- 用户明确点名 `writing-skills`。
- 希望临时使用 Superpowers 的 skill authoring discipline。

典型 case：

- 为重复工作沉淀新的 `SKILL.md`。
- 审查一个 skill 是否有清楚触发条件、步骤和验证方法。

注意事项：

- skill 应解决重复问题，不是普通文档。
- 要明确类型、目录结构、触发规则和测试方式。

## 6. 推荐组合流程

### 6.1 新功能从想法到落地

1. 项目有 `.trellis/workflow.md`：按 Trellis workflow；需要深度规划时用 `trellis-deep-planning`。
2. 项目没有 `.trellis/workflow.md`：用 `think` 明确目标、影响面、验收方式。
3. 必要时显式点名 Superpowers 子能力作为参考 discipline，但不让它维护第二套 plan 或 spec。
4. 实现后运行最小有效验证。
5. 用 `check` 做合并前 review 或 release gate。

### 6.2 Bug 或返工修复

1. 项目有 `.trellis/workflow.md`：按 Trellis debugging / break-loop flow。
2. 项目没有 `.trellis/workflow.md`：用 `hunt` 复现、收集证据、追数据流。
3. 提出假设：根因是 X，因为证据 Y；排除 Z，因为证据 W。
4. 能写回归测试就先写失败用例。
5. 最小修复：只改根因点，不混入无关重构。
6. 跑最小有效验证。
7. `check`：影响面较大时做 review。

### 6.3 设计和前端打磨

1. `design`：确认产品语境、现有风格和目标用户。
2. `colawd-ui-style`：仅当目标是 colawd 风格时叠加。
3. 实现后启动本地服务。
4. 用浏览器截图或目标产品表面验证文字、间距、响应式、交互状态。

### 6.4 研究、写作和报告

1. `read`：读单个 URL/PDF。
2. `learn`：多来源深度研究。
3. `tech-solution-radar`：需要选型、评分、推荐时使用。
4. `research-note-wrap`：沉淀为笔记。
5. `write`：润色输出，去 AI 味。

### 6.5 本机和 agent harness 维护

1. `mcp-healthcheck`：MCP server、auth、proxy、tool list 异常。
2. `health`：更高层的工程健康审计。
3. `hone`：把外部 agent coding signals 映射为本地 harness 实践。

### 6.6 会话和分支收尾

1. `commit-daily-summary` 或 `project-daily-summary`：需要日报时使用。
2. `session-handoff`：需要交接给另一个 agent 时使用。
3. 用户显式点名时，`finishing-a-development-branch` 可作为 Superpowers 分支收尾参考。

## 7. 维护规则

新增或修改 skill 时：

1. 需要 Superpowers authoring discipline 时显式点名 `writing-skills`；普通 wrapper 调整可直接遵守本文档和 `rules/codex-global.md`。
2. 在 `skills/<domain>/<skill-name>/SKILL.md` 中写清楚 `name`、`description`、触发场景、流程、验证方式。
3. 更新 `registry/skills.yaml`。
4. 若新增 domain，同步更新 `README.md` 和本文档。
5. 运行覆盖检查：

```bash
rg --files skills -g 'SKILL.md'
```

如果本文档要保持完整，`rg --files skills -g 'SKILL.md' | wc -l` 的数量应与本文档开头的 active skill 总数一致。

## 8. 常见误用

| 误用 | 正确做法 |
| --- | --- |
| 为了效率跳过 bug 复现，直接 patch 症状点 | 默认用 `hunt`，显式点名时再用 `systematic-debugging`。 |
| 用户只是要 review，却改了代码 | 用 `check` 先输出 findings；只有用户要求才修改。 |
| 对单链接阅读启动深度研究流程 | 用 `read`，只有多来源整合才用 `learn`。 |
| 把 MCP 配置问题当成通用文档问题 | 用 `mcp-healthcheck` 读取当前机器证据。 |
| 把所有 UI 都套 colawd 风格 | 只有用户要求或项目风格匹配时才用 `colawd-ui-style`。 |
| vendored skill 里直接手改流程 | 不手改 `vendor/skills/`；需要变更时改同步来源或新增本仓库 wrapper skill。 |
