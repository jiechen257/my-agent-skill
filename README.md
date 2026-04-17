# my-agent-skill

这个仓库用于集中存放多个 agent skill 源码。

## 全局 rules

仓库根目录的 [`AGENTS.md`](./AGENTS.md) 保存当前使用中的全局 rules。

其中两个历史别名已对齐为本地实际 skill 名：

- `daily-commit-summary` -> `commit-daily-summary`
- `codex-project-daily-summary` -> `project-daily-summary`

## 目录结构

```text
AGENTS.md
skills/
  architecture-diagram/
    SKILL.md
    assets/
    tests/
  research-note-wrap/
    SKILL.md
  session-wrap/
    SKILL.md
  commit-daily-summary/
    SKILL.md
  project-daily-summary/
    SKILL.md
  worktree-closeout/
    SKILL.md
```

## 当前收录

- `architecture-diagram`
- `research-note-wrap`
- `session-wrap`
- `commit-daily-summary`
- `project-daily-summary`
- `worktree-closeout`

## 来源

### 仓库内已收录

- `architecture-diagram`：仓库原有 skill
- `research-note-wrap`：<https://github.com/leonsong09/research-note-wrap>
- `session-wrap`：<https://github.com/leonsong09/session-wrap>
- `commit-daily-summary`：<https://github.com/leonsong09/commit-daily-summary>
- `project-daily-summary`：<https://github.com/leonsong09/project-daily-summary>
- `worktree-closeout`：<https://github.com/leonsong09/worktree-closeout>

以上 5 个 workflow skills 的整理入口参考：
<https://linux.do/t/topic/1854180>

### 全局 rules 依赖但未 vendored 到本仓库

- `ui-ux-pro-max`：<https://github.com/nextlevelbuilder/ui-ux-pro-max-skill/tree/main/.claude/skills/ui-ux-pro-max>
- `codex-parallel-collab`：<https://github.com/mci77777/codex-parallel-collab>

### 本地 Superpowers bundle

以下 skills 当前来自本机 `~/.codex/superpowers/skills/`，对应 GitHub 来源：
<https://github.com/obra/superpowers/tree/main/skills>

- `brainstorming`
- `writing-plans`
- `systematic-debugging`
- `requesting-code-review`
- `receiving-code-review`
- `verification-before-completion`
- `test-driven-development`

## 约定

- 每个 skill 使用独立目录：`skills/<skill-name>/`
- skill 说明文件固定为 `SKILL.md`
- 模板、脚本、测试等资源跟随各自 skill 目录存放
