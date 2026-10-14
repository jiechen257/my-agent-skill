# Trellis + Matt Profile

这里是本机 Trellis + Matt Profile 的统一模板源。目标业务项目默认只安装本地副本；只有项目被明确允许时，才提交 `.trellis/` 和 `.codex/agents/trellis-matt-*.toml`。具体项目的安装状态与版本化授权在目标项目本地维护，不在本仓库登记。

## 受管内容

- `config-overlay.yaml`：需要合并到本地 `.trellis/config.yaml` 的配置。
- `workflow-policy.md`：需要体现在本地 `.trellis/workflow.md` 的行为边界，包含实际注入的 Inline 状态块。
- `hooks.json`：安装到 `.codex/hooks.json` 的最小注册；只保留活动任务的 per-turn 状态注入。合并时保留项目独立 hooks。
- `agents/trellis-matt-implement.toml`：保留的可选实现 agent，默认不派发。
- `agents/trellis-matt-check.toml`：保留的可选 review agent，默认不派发。

全局路由规则的版本化源文件是 `rules/codex-global.md`；完整设计与调研结论位于 `docs/trellis-matt-vs-openspec-matt.md` 和 `docs/trellis-codex-subagents-2026-07-14.md`。

## 本地安装边界

1. 默认情况下，目标项目的 `.trellis/` 和 `.codex/` 必须已被项目 `.gitignore` 或本地 `.git/info/exclude` 排除。
2. 先确认该项目是 local-only 还是明确允许版本化，再把本目录的配置合并或复制到目标项目。
3. 不覆盖 task、spec、workspace、journal 或 runtime 数据。
4. local-only 项目不修改 tracked `AGENTS.md` 或生成文档来记录此 Profile；明确允许版本化的项目可同步项目级说明。
5. 若目标项目历史上已经跟踪 `.trellis/`，不要自动执行大规模 `git rm --cached`；先单独确认迁移范围。仅需保留本机 overlay 时，可对明确的配置文件使用 `git update-index --skip-worktree`，并用 `git ls-files -v` 检查本地标记。
6. 当前默认 `codex.dispatch_mode: inline`；只有用户明确要求重新启用时，才使用 `agents/` 中的子 agent 定义。

最低验证：

```bash
git check-ignore -v \
  .trellis/config.yaml \
  .trellis/workflow.md \
  .codex/agents/trellis-matt-implement.toml \
  .codex/agents/trellis-matt-check.toml

git status --short --untracked-files=all -- .trellis .codex
```

local-only 项目的期望结果：Profile 文件保持本地生效，但不会出现在目标项目的待提交文件中。明确允许版本化的项目则应看到配置、workflow 和 agent 定义进入正常 diff。

## Hook 兼容修正

现有 Trellis 的 `inject-workflow-state.py` 来自项目安装版本，不整体覆盖：

- Codex 解析活动任务后，没有任务时直接返回，不重复输出 bootstrap 和 no-task breadcrumb。
- 默认 dispatch 为 `inline`；显式启用子 agent 的兼容路径保留。活动任务、过期指针和其他客户端的响应格式继续按原脚本处理。
- 删除旧 `trellis-implement|trellis-check|trellis-research` 的 `SubagentStart` 注册。保留 agent 定义和脚本作为显式使用时的兼容资料。
- `trellis update` 可能重新生成脚本和注册。升级后复查这些修正，确认当前 Profile 和 hooks，再由 Codex 重新加载并审核实际 hash。
- 验证无任务、planning、in_progress、completed、stale 指针五种行为；验证活动上下文仍在主会话恢复。

各项目 `.trellis/workflow.md` 的 `<!-- local-trellis-matt-profile -->` 后应与 `workflow-policy.md` 一致。源模板不承载项目任务、spec 或 journal。
