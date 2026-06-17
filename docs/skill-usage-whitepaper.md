# Skill 使用手册与白皮书

更新时间：2026-06-17
适用仓库：`/Users/zhici/work-pro/my-agent-skill`

## 1. 定位

本仓库集中维护个人 Codex / Claude Code skills。`skills/` 下的每个 `SKILL.md` 都代表一个可触发的工作能力，覆盖设计、开发流程、调试、代码审查、本机维护、研究文档、会话交接和第三方流程工具。

截至本文档更新时，当前项目共有 37 个 active skill：

| 类别 | 数量 | 说明 |
| --- | ---: | --- |
| `design` | 2 | UI/UX、视觉风格、截图驱动打磨 |
| `workflow` | 4 | 方案、review、debug、决策压测 |
| `harness` | 5 | 本机、Codex、MCP、worktree、工程健康检查 |
| `research-docs` | 11 | 链接阅读、调研、日报、周报、写作、会话管理 |
| `hone` | 1 | frontier AI coding signals 与本地 agent harness 实践 |
| `vendored/superpowers` | 14 | 外部同步的通用流程 skill |

`registry/skills.yaml` 把 `vendored/superpowers` 作为一个外部同步来源登记，但目录下有 14 个独立 `SKILL.md`。本文档按实际可触发 skill 逐一说明。

## 2. 使用总原则

先判断任务类型，再选择 skill。简单任务不需要堆流程；高风险任务、返工、bug、跨模块改动必须先收集证据再行动。

使用 skill 时遵守以下顺序：

1. 确认用户请求是否显式点名 skill。
2. 若未点名，按场景匹配最接近的 skill。
3. 读取对应 `SKILL.md` 的完整内容，再执行。
4. 如果 skill 引用 `references/`、`scripts/`、`agents/`、`assets/`，只读取或运行当前任务必需的部分。
5. 修改文件前说明将改什么；修改后运行与风险匹配的验证。
6. 不还原用户已有改动；脏工作区只处理当前任务相关文件。

不要同时启动两套完整流程。比如一个 bug 修复不要同时走 `hunt`、`systematic-debugging`、`think` 三条主流程；选一个主流程，其他 skill 只作为原子方法参考。

## 3. 场景速查

| 用户意图或场景 | 首选 skill | 可组合 skill | 注意事项 |
| --- | --- | --- | --- |
| 做一个新功能、交互、组件或行为变化 | `brainstorming` 或 `think` | `writing-plans`、`test-driven-development` | 需求不清时先收敛目标、影响面、验收方式。 |
| 用户要求“出方案”“怎么设计”“有没有必要” | `think` | `grill-me` | 输出决策完整的方案，不直接写代码。 |
| 用户要被追问、压测方案 | `grill-me` | `think` | 一次问一个问题；能从代码查到的就先查。 |
| bug、异常、构建失败、测试失败 | `hunt` 或 `systematic-debugging` | `test-driven-development`、`verification-before-completion` | 先复现、追数据流、提出假设，再修复。 |
| 代码审查、合并前检查、发布前检查 | `check` | `requesting-code-review`、`verification-before-completion` | findings 先行，按严重程度排序。 |
| 接收 review 意见并准备修改 | `receiving-code-review` | `systematic-debugging` | 不盲从 review，先验证反馈是否成立。 |
| UI 设计、页面打磨、截图复刻 | `design` | `colawd-ui-style` | 先确认产品语境和现有风格，不做泛化模板页。 |
| 复刻 colawd 风格工作台 | `colawd-ui-style` | `design` | 保持黑色 shell、浅黄网格、粗边框、硬阴影等风格约束。 |
| 本机 Codex/Claude/MCP 配置异常 | `codex-local-maintenance`、`mcp-healthcheck` | `health` | 以当前机器证据为准，先诊断再改配置。 |
| Mac 卡顿、登录项、缓存、shell 慢 | `mac-system-optimizer` | `codex-local-maintenance` | 破坏性清理前必须确认；先分类风险。 |
| 多 worktree 或并行分支收口 | `worktree-closeout` | `session-handoff` | 先按日期和范围扫描，再给合并/归档顺序。 |
| 今天做了什么、提交日报 | `commit-daily-summary` | `project-daily-summary` | commit 证据优先，不用记忆替代 git。 |
| 按项目总结今天所有 Codex 工作 | `project-daily-summary` | `session-wrap` | 同时看会话、提交和未提交变更。 |
| 周报 | `weekly-report-template` | `commit-daily-summary` | 只覆盖用户指定 repo 和时间段。 |
| 读链接、读 PDF、转 Markdown | `read` | `research-note-wrap` | 外部最新信息要实时验证并保留来源。 |
| 深入研究、整合资料成文章 | `learn` | `tech-solution-radar`、`write` | 适合多来源，不适合单个快速查找。 |
| 技术选型、工具对比、最佳实践调研 | `tech-solution-radar` | `read`、`research-note-wrap` | 给证据、评分和推荐，不只罗列优缺点。 |
| 润色、改稿、去 AI 味 | `write` | `read` | 保留原意，不虚构事实。 |
| 总结调研为 Obsidian 笔记 | `research-note-wrap` | `learn` | 明确输出位置和范围。 |
| 会话收尾 | `session-wrap` | `commit-daily-summary` | 输出完成项、决策、开放问题和下一步。 |
| 写交接 prompt 给另一个 agent | `session-handoff` | `worktree-closeout` | 生成自包含交接文件，不泄露密钥。 |
| 判断知识应该写到哪里 | `memory-routing` | `research-note-wrap` | 区分 Codex memory、repo docs、Yuque/DingTalk、日报。 |
| frontier AI coding / hone 相关讨论 | `hone` | `health` | 聚焦 signals、harness drift 和本地实践映射。 |
| 多个独立子任务可并行 | `dispatching-parallel-agents` | `subagent-driven-development` | 必须保证子任务边界独立。 |
| 已有书面计划，需要执行 | `executing-plans` | `subagent-driven-development` | 按计划任务执行，并保留 review checkpoints。 |
| 开始需要隔离的功能分支 | `using-git-worktrees` | `writing-plans` | 先检查是否已有隔离工作区。 |
| 完成开发分支，准备合并或 PR | `finishing-a-development-branch` | `verification-before-completion` | 先验证测试，再选择 merge、PR 或清理。 |
| 创建或修改 skill | `writing-skills` | `test-driven-development` | skill 本身也要有触发场景、流程和验证方式。 |

## 4. 自维护 skills

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

### 4.7 `codex-local-maintenance`

路径：`skills/harness/codex-local-maintenance/SKILL.md`

适用场景：

- 检查、更新、排查本机 Codex CLI/Desktop。
- 版本、Bun global install、代理、first-token latency、日志、launcher/state 异常。

典型 case：

- Codex 启动慢或连接不稳定。
- Codex Desktop 和 CLI 行为不一致。
- 需要确认当前实际加载的全局规则和配置。

注意事项：

- 以当前机器证据为准，不从泛泛文档推断。
- 修改本机配置前先备份或说明影响面。

### 4.8 `mac-system-optimizer`

路径：`skills/harness/mac-system-optimizer/SKILL.md`

适用场景：

- Mac 性能、响应、开发工作流、shell 启动、浏览器内存、登录项、LaunchAgents、Docker/Homebrew 缓存。

典型 case：

- 找出导致机器卡顿的进程和登录项。
- 清理开发缓存。
- 优化 zsh 启动耗时。

注意事项：

- 证据优先诊断。
- 破坏性动作和禁用登录项前要确认。
- 每个改动后验证效果。

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

### 4.11 `worktree-closeout`

路径：`skills/harness/worktree-closeout/SKILL.md`

适用场景：

- 多 Codex session、多 worktree、多分支并行后需要收口。
- 用户说“worktree 收口”“分支收口”“并行收口”。

典型 case：

- 扫描某天打开的 worktree。
- 判断哪些可以 merge、哪些需要归档、哪些要继续交接。
- 给每个未完成分支生成 prompt-ready handoff。

注意事项：

- 先问日期，再问范围。
- 运行 scanner 后读 artifact，不凭记忆判断。

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

### 4.17 `memory-routing`

路径：`skills/research-docs/memory-routing/SKILL.md`

适用场景：

- 判断长期知识该放到 Codex memory、Basic Memory MCP、repo docs、DingTalk/Yuque、daily reports 还是 project notes。

典型 case：

- 用户要求“记住这个”或“这个应该沉淀在哪里”。
- 把一次会话里的可复用约定拆成合适的存储位置。

注意事项：

- 区分个人偏好、项目事实、临时结果和外部资料。
- 只有用户明确要求时才更新 memory。

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

### 4.20 `session-wrap`

路径：`skills/research-docs/session-wrap/SKILL.md`

适用场景：

- 用户要结束会话、总结本次 coding session、决定是否提交、提取 learnings 和 open items。

典型 case：

- 本轮开发收尾。
- 给用户列出完成项、关键决策、剩余风险、下一步。

注意事项：

- 先确认 scope。
- 必须检查工作树，避免遗漏未提交改动。

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

## 5. Vendored Superpowers skills

这些 skill 位于 `skills/vendored/superpowers/`，由外部源同步。使用时应遵循其 `SKILL.md`，但不要在本仓库手动修改 vendored 内容。

### 5.1 `using-superpowers`

路径：`skills/vendored/superpowers/using-superpowers/SKILL.md`

适用场景：

- 会话开始时进行 skill 路由自检。
- 判断是否有任何 skill 应该参与当前任务。

注意事项：

- 它强调先查 skill 再行动。
- 若与用户明确规则或上层系统规则冲突，以上层规则为准。

### 5.2 `brainstorming`

路径：`skills/vendored/superpowers/brainstorming/SKILL.md`

适用场景：

- 创意工作、新功能、组件、行为修改前理解用户意图和设计。

典型 case：

- 从模糊 idea 收敛出设计。
- 提供 2 到 3 个方案并选择推荐方向。

注意事项：

- 原 skill 有严格 approval gate；在本仓库使用时要同时遵守用户全局 AGENTS 的任务分流规则。
- 对轻量任务可以保留“先看上下文、明确 DoD”的核心，不应机械扩大流程。

### 5.3 `writing-plans`

路径：`skills/vendored/superpowers/writing-plans/SKILL.md`

适用场景：

- 已有 spec 或明确需求，需要写多步骤实施计划。

典型 case：

- 把批准的方案拆成 bite-sized implementation tasks。
- 为另一个 agent 写可执行计划。

注意事项：

- 不要写占位符。
- 计划要包含文件、改动、测试和交接说明。

### 5.4 `executing-plans`

路径：`skills/vendored/superpowers/executing-plans/SKILL.md`

适用场景：

- 已有书面计划，需要按计划执行，并带 review checkpoints。

典型 case：

- 在独立 session 中执行 implementation plan。
- 执行过程中发现计划过期，需要回到早期步骤。

注意事项：

- 先加载并审查计划。
- 遇到阻塞要停下来说明，不要静默改计划。

### 5.5 `test-driven-development`

路径：`skills/vendored/superpowers/test-driven-development/SKILL.md`

适用场景：

- 实现功能或 bugfix 前能写自动化测试。

典型 case：

- 为回归 bug 写失败用例。
- 为纯函数、边界条件、关键业务逻辑加测试。

注意事项：

- 遵守 red、green、refactor 顺序。
- 如果无法写测试，要说明原因并给替代验证。

### 5.6 `systematic-debugging`

路径：`skills/vendored/superpowers/systematic-debugging/SKILL.md`

适用场景：

- 任何 bug、测试失败、异常行为，在提出修复前使用。

典型 case：

- 先找 root cause，再修复。
- 验证假设后实施最小改动。

注意事项：

- 四阶段：root cause investigation、pattern analysis、hypothesis and testing、implementation。
- 不允许“看起来像”就修。

### 5.7 `verification-before-completion`

路径：`skills/vendored/superpowers/verification-before-completion/SKILL.md`

适用场景：

- 准备声称工作完成、测试通过、问题修复、提交或 PR 前。

典型 case：

- 最后跑 lint、typecheck、unit test、build。
- 前端任务做浏览器或截图验证。

注意事项：

- 证据先于结论。
- 如果验证失败或无法运行，必须明确说明。

### 5.8 `requesting-code-review`

路径：`skills/vendored/superpowers/requesting-code-review/SKILL.md`

适用场景：

- 完成主要功能、准备合并前请求 review。

典型 case：

- 把变更摘要、测试结果、风险点交给 reviewer。

注意事项：

- 不要在明显缺少验证时请求 review。

### 5.9 `receiving-code-review`

路径：`skills/vendored/superpowers/receiving-code-review/SKILL.md`

适用场景：

- 收到 review feedback 后准备处理。

典型 case：

- 判断反馈是否正确、是否值得做、是否需要反驳。
- 对不清晰反馈做 technical clarification。

注意事项：

- 不盲目接受。
- 不用“professional-looking”改动扩大范围。

### 5.10 `dispatching-parallel-agents`

路径：`skills/vendored/superpowers/dispatching-parallel-agents/SKILL.md`

适用场景：

- 有两个以上互不依赖的任务，可并行分派。

典型 case：

- 一个 agent 查 API，一个 agent 查 UI，一个 agent 查测试。
- 多 repo 独立扫描。

注意事项：

- 子任务必须边界清楚、无共享写状态。
- 主 agent 负责整合和冲突处理。

### 5.11 `subagent-driven-development`

路径：`skills/vendored/superpowers/subagent-driven-development/SKILL.md`

适用场景：

- 执行实现计划时，当前 session 内有多个独立 implementation tasks。

典型 case：

- 拆分实现、测试、文档子任务。

注意事项：

- 不适合高度耦合或需要连续上下文的改动。
- 子 agent 结果必须由主 agent 审核。

### 5.12 `using-git-worktrees`

路径：`skills/vendored/superpowers/using-git-worktrees/SKILL.md`

适用场景：

- 开始需要隔离的功能工作，或执行 implementation plan 前。

典型 case：

- 当前 worktree 有用户未提交改动，不能直接改。
- 多个 feature 并行。

注意事项：

- 先检测是否已有隔离环境。
- 使用 native worktree tools 或 git worktree fallback。

### 5.13 `finishing-a-development-branch`

路径：`skills/vendored/superpowers/finishing-a-development-branch/SKILL.md`

适用场景：

- 实现完成、测试通过，需要决定 merge、PR、cleanup。

典型 case：

- 分支收尾时给用户结构化选项。

注意事项：

- 先验证测试，再判断 base branch 和集成路径。
- 不要擅自做破坏性 cleanup。

### 5.14 `writing-skills`

路径：`skills/vendored/superpowers/writing-skills/SKILL.md`

适用场景：

- 创建新 skill、修改已有 skill、验证 skill 部署前质量。

典型 case：

- 为重复工作沉淀新的 `SKILL.md`。
- 审查一个 skill 是否有清楚触发条件、步骤和验证方法。

注意事项：

- skill 应解决重复问题，不是普通文档。
- 要明确类型、目录结构、触发规则和测试方式。

## 6. 推荐组合流程

### 6.1 新功能从想法到落地

1. `think` 或 `brainstorming`：明确目标、影响面、验收方式。
2. `writing-plans`：把批准方案拆成可执行任务。
3. `using-git-worktrees`：必要时隔离工作区。
4. `test-driven-development`：能测试的先写失败用例。
5. `executing-plans` 或直接实现：按计划执行。
6. `verification-before-completion`：验证后再声称完成。
7. `check` 或 `requesting-code-review`：合并前 review。

### 6.2 Bug 或返工修复

1. `hunt` 或 `systematic-debugging`：复现、收集证据、追数据流。
2. 提出假设：根因是 X，因为证据 Y；排除 Z，因为证据 W。
3. `test-driven-development`：能写回归测试就先写失败用例。
4. 最小修复：只改根因点，不混入无关重构。
5. `verification-before-completion`：跑最小有效验证。
6. `check`：影响面较大时做 review。

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

1. `codex-local-maintenance`：Codex CLI/Desktop 或规则加载异常。
2. `mcp-healthcheck`：MCP server、auth、proxy、tool list 异常。
3. `mac-system-optimizer`：系统性能和开发环境性能。
4. `health`：更高层的工程健康审计。
5. `hone`：把外部 agent coding signals 映射为本地 harness 实践。

### 6.6 会话和分支收尾

1. `session-wrap`：总结当前会话、完成项、决策、开放问题。
2. `commit-daily-summary` 或 `project-daily-summary`：需要日报时使用。
3. `worktree-closeout`：多 worktree、多分支需要收口时使用。
4. `session-handoff`：需要交接给另一个 agent 时使用。
5. `finishing-a-development-branch`：准备 merge/PR/cleanup 时使用。

## 7. 维护规则

新增或修改 skill 时：

1. 使用 `writing-skills`。
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
| 为了效率跳过 bug 复现，直接 patch 症状点 | 用 `hunt` 或 `systematic-debugging` 先确认根因。 |
| 用户只是要 review，却改了代码 | 用 `check` 先输出 findings；只有用户要求才修改。 |
| 对单链接阅读启动深度研究流程 | 用 `read`，只有多来源整合才用 `learn`。 |
| 把本机配置问题当成通用文档问题 | 用 `codex-local-maintenance` 或 `mcp-healthcheck` 读取当前机器证据。 |
| 把所有 UI 都套 colawd 风格 | 只有用户要求或项目风格匹配时才用 `colawd-ui-style`。 |
| vendored skill 里直接手改流程 | 不手改 `skills/vendored/`；需要变更时改同步来源或新增本仓库 wrapper skill。 |
| memory、日报、repo docs 混用 | 用 `memory-routing` 判断知识归属。 |
