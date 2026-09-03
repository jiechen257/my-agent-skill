# Skill Usage Guide

本仓库当前只把 `skills/` 下的 wrapper 作为 active skill。`vendor/skills/` 只是同步源快照，不直接安装。

## 当前主线

- 简单任务：Inline，直接完成并做最小验证。
- 通用工程流程：Matt Pocock engineering/productivity skills。
- Trellis + Matt Profile：Trellis 管理任务/上下文并保留 brainstorm；Matt 提供规划 review、实现、TDD、诊断和 code-review 方法。

## 常用路由

| 场景 | 默认 skill |
| --- | --- |
| 不知道该走哪个 Matt flow | `ask-matt` |
| Trellis 需求探索 | `trellis-brainstorm` |
| Trellis 方案完成后的压力 review | `grill-me` |
| 非 Trellis 需求或设计需要拷问 | `grill-with-docs` / `grill-me` |
| 当前对话沉淀成 PRD | `to-prd` |
| PRD / 计划拆成任务 | `to-issues` |
| 基于 PRD / issue 实现 | `implement` |
| 行为变更或 bugfix 先写测试 | `tdd` |
| bug、报错、回归、性能问题 | `diagnosing-bugs` |
| review 本地变更或 PR | `code-review` |
| issue / PR 队列分流 | `triage` |
| 模块边界、接口、可测试性 | `codebase-design` |
| 领域词汇、ADR、业务概念 | `domain-modeling` |
| 临时验证设计想法 | `prototype` |
| 技术调研并沉淀资料 | `research` |
| merge / rebase 冲突 | `resolving-merge-conflicts` |
| 会话交接 | `handoff` |

## 安装面

`registry/skills.yaml` 控制安装：

- `repo-managed` + `codex: true`：安装到 `~/.codex/skills/`。
- `repo-managed` + `claude: true`：安装到 `~/.claude/skills/`。
- `vendored`：只供 `scripts/sync-vendored-skills.sh` 同步，不直接安装。

Matt Pocock wrapper 当前只打开 `codex: true`，避免本次 Codex 重构顺手改 Claude。

## Trellis 使用方式

Trellis 负责生命周期，Matt 负责工程方法：

1. 进入或恢复项目：`trellis-start` / `trellis-continue`。
2. 规划：`trellis-brainstorm` 写 task artifacts，`grill-me` 做最终 review gate。
3. Codex 实现：默认在主会话应用 Matt implement/TDD 方法并完成检查，不主动派发子 agent。
4. 主会话验收后，只在有稳定知识且用户确认时执行 `trellis-update-spec`。
5. `trellis-finish-work` 归档并记录；不自动 commit。

保留的 `trellis-matt-*` 定义仅作为回滚能力，只有用户明确要求时才启用。commit、push、PR 也只在用户明确要求时执行。
