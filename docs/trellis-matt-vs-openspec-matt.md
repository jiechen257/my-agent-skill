# Trellis + Matt 与 OpenSpec + Matt：结合两篇实践文章的复核

> 调研日期：2026-07-13
> 问题：如果 Trellis 只负责记录 spec、task 和跨会话上下文，Matt Skills 负责实现、诊断、TDD 和 review，是否比 OpenSpec + Matt 更适合？

## 结论

你的感觉有依据。**如果你真正想保留的不只是 `spec.md` 和 `tasks.md`，还包括当前任务指针、跨会话恢复、任务历史、journal 和按需上下文注入，那么“裁剪后的 Trellis + Matt”比 OpenSpec + Matt 更贴合。**

但这里的准确方案不是“默认 Trellis + 全套 Matt”，而是一个明确分工的 Trellis + Matt Profile：

- Trellis 作为 **state/context and planning store**：保存 `.trellis/spec/`、`.trellis/tasks/`、`.trellis/workspace/`，负责 brainstorm、start、resume 和 archive。
- Matt 作为 **engineering method layer**：`grill-me` review、实现、TDD、诊断和 code review 方法由 Matt 提供。
- Codex 默认在主会话应用 Matt 的 implement/TDD/review 方法；`trellis-matt-*` 仅保留为显式启用的回滚资产。
- 保留的 Trellis hook 只注入紧凑的任务状态和索引，不把完整工作流反复塞进每轮上下文。

这是一套 **Trellis + Matt Profile**，不是 Trellis 的零配置默认模式。版本化模板源统一由当前 `my-agent-skill/templates/trellis-matt-profile/` 管理；业务项目默认只保留本机安装副本，只有明确允许的项目才提交 `.trellis/` 和 Profile agent。当前 personal-kb 允许版本化，qianwen、nexview-devtools 保持本地-only。Trellis 升级后需要在模板源复核 workflow policy、skills、agents 和 hooks，再更新各项目副本。

因此，local-only 项目中的 task、journal 和 active-task 恢复只是本机持久状态，不天然具备 Git 团队共享能力；允许版本化的项目则可以继续共享 task/spec 历史。需要团队长期共享的稳定知识仍应优先进入项目正常文档体系。

如果你只需要“proposal / design / spec / tasks 的变更生命周期”，不关心 journal、active task 和自动恢复，那么 OpenSpec + Matt 仍然更干净、维护成本更低。

## 两篇文章真正说明了什么

### 1.《Trellis + grill-me 组合用起来很爽》

[原文](https://linux.do/t/topic/2084756)描述的是：先用极简的 `grill-me` 把需求问清楚，再把后续工作交给 Trellis。作者看中的组合方式是：

1. `grill-me` 负责高质量需求澄清，而且能嵌入现有 workflow。
2. Trellis 接管澄清之后的任务资产、执行和交付闭环。
3. 相比一个从 brainstorm 到交付都强制接管的框架，这种组合更灵活。

需要注意：这篇文章验证的是 **grill-me + 默认 Trellis 执行链**，并没有验证“完整 Matt 工程技能集 + Trellis”。如果再加入 Matt 的 `implement`、`tdd`、`diagnosing-bugs`、`code-review`，就会与 Trellis 的 implement/check 阶段产生重叠，必须先做路由裁剪。

### 2.《从 vibe coding 到 spec coding：我用 Trellis 的实践总结》

[原文](https://linux.do/t/topic/2571606)把 Trellis 的价值归纳为三个问题的解决方案：

- 会话失忆：task、workspace、journal 和启动上下文让新会话能恢复现场。
- 工具切换：不同 agent 共用 `.trellis/` 中的 spec、task 和 workflow 事实源。
- 项目级闭环：spec、task、workflow-state、check、update-spec、archive 和 journal 连成一个生命周期。

这篇文章最有价值的判断是：**rules 和 skills 主要告诉 agent“怎么做”，但并不天然记录“当前做到哪里、为什么这样做、下次从哪里继续”。** 这正是 Trellis 相对 OpenSpec 和 Matt 的差异化能力。

文章也明确承认 Trellis 的成本：它需要维护 spec、控制 task 粒度，并且不同平台的 hooks 和 skills 体验不同。它适合长期维护、多决策、需要交接或频繁切换会话的项目，不适合一次性脚本和小修改。

## 与官方资料交叉核对

### Trellis 的确提供持久上下文，但默认是完整 harness

Trellis 官方把自身定义为 Agent Harness 加内置 LLM wiki。其持久工件包括：

| 工件 | 官方职责 |
|---|---|
| `.trellis/spec/` | 团队规范、模块规则和可复用经验 |
| `.trellis/tasks/` | PRD、research、任务状态、implement/check 上下文清单和归档历史 |
| `.trellis/workspace/<developer>/` | 开发者 journal 与跨会话工作记忆 |
| `.trellis/workflow.md` | phase、路由和每轮 workflow-state 契约 |

来源：[Trellis README](https://github.com/mindfold-ai/Trellis#why-trellis)、[Architecture Overview](https://docs.trytrellis.app/advanced/architecture)、[How It Works](https://docs.trytrellis.app/start/how-it-works)。

但官方默认路由是 Plan → Implement → Verify → Finish，并会调用 brainstorm、implement、check、update-spec 等能力。因此，“Trellis 只负责记录”不是默认 profile，而是本地定制。

官方允许修改 `.trellis/workflow.md`，包括调整 phase、skill routing 和 workflow-state；因此裁剪是受支持的扩展方式，而不是逆向 hack。参考：[Custom Workflow](https://docs.trytrellis.app/advanced/custom-workflow) 和 [FAQ / Appendix F](https://docs.trytrellis.app/advanced/appendix-f)。不过官方同时建议一个 session 不要并行运行两个 phase controller，这正是必须明确唯一 workflow owner 的原因。

还有一个值得校正的点：第二篇文章把“小 bug 可以自然 inline”描述得较宽松，但当前官方文档的默认规则更严格——只读回答可直接完成，产生文件改动的工作默认创建 Trellis task；inline 是用户显式要求跳过 Trellis时的 escape hatch。实际使用是否轻量，取决于你对 `.trellis/workflow.md` 的裁剪，而不只是 agent 自己判断任务大小。[How It Works](https://docs.trytrellis.app/start/how-it-works)

### OpenSpec 更像 change artifact lifecycle，而不是项目工作记忆

OpenSpec 的核心结构是：

- `openspec/specs/`：当前系统行为的 source of truth。
- `openspec/changes/<name>/proposal.md`：为什么改、改什么。
- change 内的 delta specs、`design.md` 和 `tasks.md`。
- 完成后 sync 到主 specs，再 archive change。

来源：[OpenSpec README](https://github.com/Fission-AI/OpenSpec)、[Concepts](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md)、[Workflows](https://github.com/Fission-AI/OpenSpec/blob/main/docs/workflows.md)。

它的优势是工件结构清晰、change 之间隔离、与 Git/PR 配合自然，而且 OpenSpec 本身不接管 commit、branch、push。[Team Workflow](https://github.com/Fission-AI/OpenSpec/blob/main/docs/team-workflow.md)

但 OpenSpec 的主要模型是“某项系统行为如何变更”，不是“某个开发者上次做到哪里”。官方 workflow 有 tasks 状态和变更归档，但没有 Trellis 那套 developer journal、session active-task pointer 与每轮 workflow-state 注入。

另外：

- `explore` 是讨论模式，官方明确说它不是 generator，不创建工件；需要持久化仍要进入 propose/new 等流程。[Explore](https://github.com/Fission-AI/OpenSpec/blob/main/docs/explore.md)
- `apply` 明确负责写代码、运行验证并勾选 tasks；如果 Matt 负责实现，就不应该再让 OpenSpec `apply` 主控。[Commands](https://github.com/Fission-AI/OpenSpec/blob/main/docs/commands.md)

### Matt 已有文档输出，但不是统一的项目状态系统

当前 Matt 官方技能已经不只是临时对话：

- `grill-with-docs` 会在需求澄清时沉淀领域词汇和 ADR。[grill-with-docs](https://github.com/mattpocock/skills/blob/main/skills/engineering/grill-with-docs/SKILL.md)
- `to-spec` 能把当前讨论整理成 spec，并发布到配置的 issue tracker。[to-spec](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-spec/SKILL.md)
- `to-tickets` 能把工作拆成 tracker tickets；本地模式也可以写 Markdown。[to-tickets](https://github.com/mattpocock/skills/blob/main/skills/engineering/to-tickets/SKILL.md)
- `implement`、`tdd`、`code-review` 等技能负责具体工程方法。[Matt Skills README](https://github.com/mattpocock/skills)

因此“Matt 没有 spec/task 能力”并不准确。更准确的说法是：Matt 把工件发布到 tracker 或项目文档，并强调小而可组合的 skills；它没有 Trellis 的统一 active task、journal、archive、workflow-state 和自动上下文恢复层。

## 针对你的方案对比

| 维度 | Trellis + Matt Profile | OpenSpec + Matt |
|---|---|---|
| 长期 spec | 强，既能放项目规范，也能沉淀经验 | 强，更偏系统行为与变更 delta |
| task 文档 | PRD、research、状态、上下文 manifest、归档 | proposal、design、spec delta、tasks |
| 跨会话恢复 | 强：active task、workspace、journal、启动上下文 | 弱：主要依赖读取 change 目录或人工指定 change |
| 自动上下文注入 | 有，但要控制 hook 注入长度和路由 | 主要依赖显式调用 workflow skill |
| 与 Matt 的职责重叠 | 默认高；裁剪后低 | `apply`/`verify` 有重叠；不安装或不调用即可 |
| 默认重量 | 较重 | 较轻 |
| 定制维护成本 | 较高，要维护 workflow fork 与 hooks | 较低，custom profile 即可 |
| Git 边界（本机 Profile） | 默认不提交；明确允许的项目可版本化，模板集中在 `my-agent-skill` | 通常随项目提交 change artifacts |
| 最适合 | 长期项目、频繁换会话、重视经验回流和任务连续性 | 只需要正式 spec/change lifecycle 的项目 |

## 推荐落地边界

如果恢复 Trellis，我建议只采用以下能力：

以下 `.trellis/*` 工件默认指目标项目的本机运行副本；明确允许版本化的项目可提交这些工件。Profile 模板本身由 `templates/trellis-matt-profile/` 持久化。

### 保留

- `.trellis/spec/`：只放稳定、可复用的项目约束，不放一次性任务事实。
- `.trellis/tasks/`：保存 PRD/spec、research、验收标准、状态和归档记录。
- `.trellis/workspace/`：保存精简 journal，用于跨会话恢复。
- session start / `trellis-start`：只注入项目索引、活动任务、最近 journal 摘要。
- `trellis-continue`：只负责读取状态和建议下一步，不自动切换到 Trellis implement/check。
- `trellis-finish-work`：只做状态归档、journal 和可复用经验候选整理。
- `trellis-update-spec`：仅在用户确认后沉淀稳定经验。

### 改写

- `trellis-brainstorm`：保留为规划 owner；完成后由 `grill-me` 做进一步 review，不重新规划。
- `trellis-implement`：Codex 下不派发子 agent，由主会话采用 Matt implement / TDD 方法且不自动 commit。
- `trellis-check`：Codex 下由主会话执行 standards/spec 双轴 review；保留的 `trellis-matt-check` 只用于未来显式恢复。
- Trellis research：与主会话 Matt `research` 二选一；结果仍写回当前 task。
- “所有写操作必须建 task”的默认规则：改成只有需要长期恢复、多个决策或跨文件阶段管理的工作才建 task。
- 每轮完整 workflow 注入：缩减为状态、当前 task 路径和下一步提示。

建议写成一句总原则：

> Trellis owns project state and planning artifacts; Matt supplies engineering methods. Codex keeps implementation, review, and final acceptance in the main session unless the user explicitly enables a sub-agent.

## 最终判断

两篇文章改变的不是“OpenSpec 和 Trellis 谁更先进”，而是比较维度：

- 如果比较 **spec/change 工件是否轻量清晰**，OpenSpec 更好。
- 如果比较 **项目是否拥有可恢复的任务状态和工作记忆**，Trellis 更完整。

你的原始诉求口头上是“记录 spec 和 task”，但从你对文章的认同看，真正需要的很可能是：

> 让新会话自动知道当前项目规范、正在做什么、上次为什么停在这里，以及这次结束后该留下什么。

这比 OpenSpec 的 artifact lifecycle 多了一层 session continuity。按这个真实需求，**Trellis + Matt Profile 是更合适的选择**；前提是同时调整全局 rules、项目 workflow、Codex agent 和 git/spec 边界，不能只靠一句全局声明覆盖持续注入的默认 workflow。
