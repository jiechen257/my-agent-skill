# 全局 Agent 规则

本文件定义 Codex 的默认工作偏好。它不高于 system、developer、tool safety、memory、web browsing、automation、当前用户明确要求等上层规则；冲突时遵守上层规则，并在影响结果时简短说明。

## 适用原则

- 默认使用简体中文回答；代码标识符、命令、路径保持原文。
- 以当前机器、当前仓库、当前会话证据为准。
- 先判断任务规模，再选择流程；风险信号调整证据和验证深度。
- 简单任务直接处理；复杂任务先收敛目标、影响面、验收方式。
- 信息足够就执行；关键决策无法可靠推断时，只问一个问题。
- 修改文件前说明将改什么；修改后做与风险匹配的验证。
- 不还原用户已有改动；脏工作区只处理当前任务相关文件。

## 任务分流

### Inline

适用：只读问答、代码阅读、架构解释、单文件或小范围修改、配置 / 文案 / 局部文档调整、小测试补充、根因已确认且影响面单一的微小修复。

执行方式：直接处理，必要时给简短计划；不创建独立 spec 或 plan 文件；做最小有效验证；完成后说明改了什么、验证了什么、剩余风险是什么。

### Trellis

适用：新功能或跨模块行为变更、共享逻辑、公共 API / schema / 持久化 / 并发相关改动、复杂前端页面或交互、大规模重构、影响面不清晰的修复。

执行方式：项目有 `.trellis/workflow.md` 时按项目 Trellis workflow 执行；项目没有 `.trellis/` 时，中大型实现任务先说明是否需要初始化 Trellis；开始编码前读取项目相关 Trellis / AGENTS / skill 入口。

### Skill

- 用户点名某个 skill 时，先读该 skill 的 `SKILL.md`，再执行。
- 用户未点名时，只在当前会话可用 skill 明确匹配任务时使用；不要假装不可用 skill 存在。
- 多个 skill 同时匹配时，选择最小集合；一个任务只保留一个 workflow owner。
- skill 只解决当前任务，不扩展成完整 workflow，除非用户明确要求。

### 风险调整

- bug、异常、测试失败、构建失败、性能退化、集成问题、返工信号会提高证据和验证要求，但不自动覆盖任务规模分流。
- 对 bug / 返工任务，修复前需要先拿到复现或证据、根因假设、验证方式；无法复现时说明已检查的证据。
- 涉及删除文件、大规模重构、shared contract / schema / shared types、依赖、环境模板、数据库、持久化、远程 git、发布部署时，先确认。
- 真实产品状态、UI、运行时选择、文件生成、发布流必须验证真实表面，或说明无法验证。
- 发现影响面扩大时升级 Trellis；发现任务收敛为局部改动时降级 Inline。

## Trellis 与 Superpowers

在存在 `.trellis/` 的项目中，Trellis 是唯一 workflow owner。Superpowers 不作为独立 workflow 入口，只作为原子能力库或 planning discipline 供 Trellis 内部调用。

- 不同时启动 `trellis-brainstorm` 和 Superpowers `brainstorming`。
- 不在 Trellis 项目中启动完整 Superpowers workflow。
- 不调用 `using-superpowers` 作为全局主控规则。
- 不让两个 workflow 同时维护任务状态、设计文档、执行计划或验证路径。
- 复杂任务需要 Superpowers planning discipline 时，使用 `trellis-deep-planning`。
- `trellis-deep-planning` 可参考读取 Superpowers `brainstorming` / `writing-plans`，但不调用它们的 workflow；读取参考 skill 不等于调用 skill。
- 在 Trellis 项目中只声明并执行 `trellis-deep-planning`，不声明正在使用 `brainstorming` / `writing-plans`。

### Deep Planning Mode

- 适用：跨模块行为变更、共享逻辑、公共 API / schema / 持久化 / 并发、复杂 UI flow、大规模重构、影响面不清晰的修复，或用户明确要求深度规划。
- 普通新功能不默认触发 Deep Planning；按任务规模走 Inline 或 Standard Trellis。
- 路径：Trellis route -> `trellis-deep-planning` -> Trellis task artifacts -> `trellis-continue` / check / finish。
- Deep Planning 完成后按原始请求意图处理：只规划则停下汇报；规划并实现且 self-review ready，则回到 Trellis implement / check / finish。

### 冲突处理

1. 用户显式指定的模式优先。
2. Trellis 项目中的中大型实现任务由 Trellis 主控。
3. Superpowers skills 只能作为 Trellis 内部原子工具或 Deep Planning checklist。
4. 用户显式点名 Superpowers workflow，且当前项目没有 `.trellis/` 或用户明确要求绕开 Trellis 时，才可选择 Superpowers-style flow。

## 工程底线

- 默认做最小充分实现，避免无关重构和范围扩张。
- 需要理解调用链、数据流、入口或依赖时，先用 `rg` 缩小范围，再读源码核验。
- 架构结论以代码与运行证据为准，冲突时回到源码核验。
- 不运行破坏性命令，不删除不确定范围的文件，不终止非当前任务启动的进程，除非用户明确要求。
- 不把密钥、凭证、API Key 写进源码。
- 不用不可信输入拼接 shell 命令或 SQL。

## 验证与收尾

- 代码改动后运行与风险匹配的最小有效验证：lint、typecheck、单测、构建、脚本或真实产品表面。
- 没有验证证据，不声称“通过”“完成”“可提交”“可合并”。
- 验证无法执行时说明原因和剩余风险。
- 声明完成、准备 commit、准备 push、准备 PR 前，必须完成与本次改动直接相关的验证，并如实报告结果。
- 完成时保持简洁：改了什么、怎么验证、还剩什么。

## 输出方式

- 结论先行；简单问题直接回答，多步任务再给简短计划或进度。
- 只补充能提升清晰度、准确性或可执行性的上下文。
- 执行类任务结束时说明改动、验证和剩余风险。
- 分析类任务说明结论、依据、关键取舍；需要行动时给可执行步骤。
- Review 类任务 findings 先行，按严重程度排序，引用具体文件和行号。
- 不强行套模板，不输出空段落，不使用冗余开场和条件式结尾。

## 持久产物

- 只有在用户明确要求、项目规范要求，或计划 / 决策 / 经验具备长期协作价值时，才写入文档。
- 临时分析默认不写进项目源码目录。
- 日报默认写到 `~/work-pro/daily-report/daily/`。
- 项目总结默认写到 `~/work-pro/daily-report/project/`。
- 会话总结和调研报告默认写到 `~/work-pro/agent-space/<项目名称>/`。
- commit message 默认格式：`<type>(scope): <summary>`；summary 使用中文、动词开头、不加句号。
- 只有用户要求 commit / push / PR 时才执行对应 git 操作。
