# my-agent-skill

集中存放个人 Codex / Claude Code skills，采用分域目录组织，便于同步、检索和接入不同 Agent 工具。

## 目录结构

```text
my-agent-skill/
├── README.md
├── install.sh             # 幂等安装脚本，链接 skill 到 ~/.claude/skills/ 和 ~/.codex/skills/
├── registry/
│   └── skills.yaml        # skill 清单（repo-managed / vendored）
├── rules/
│   └── codex-global.md    # 全局 Codex AGENTS.md 源文件（手动部署）
├── scripts/
│   ├── audit-global-skills.sh
│   └── sync-vendored-skills.sh
├── skills/
│   ├── design/            # 设计、UI、图表
│   ├── workflow/           # 开发流程辅助（review、debug、方案、压测）
│   ├── harness/           # 本机维护、健康检查、worktree 管理
│   ├── research-docs/     # 调研、文档、报告、会话管理
│   └── vendored/          # 外部同步的 skill 集合（如 superpowers）
├── prompts/
│   └── best-prompts/      # 个人收藏的 prompt 模板（不参与自动化，手动引用）
└── templates/
    ├── SKILL.template.md
    └── SKILL.with-references.template.md
```

## 约定

- 真实可用的 skill 只放在 `skills/` 下。
- 每个 skill 使用独立目录：`skills/<domain>/<skill-name>/`。
- 每个 skill 必须包含一个 `SKILL.md`，可按需附带 `agents/`、`references/`、`scripts/`、`assets/`。
- `templates/` 只放可复用骨架，不作为 active skill。
- `prompts/` 存放个人收藏的 prompt 模板，供手动复制使用，不参与 install 或 registry。
- `rules/` 存放全局 agent 规则源文件，手动部署到目标位置（如 `~/.codex/AGENTS.md`）。
- domain 只表达稳定分类，避免把临时项目名放到 domain 层。
- skill 文件里不写密钥、token、机器专属凭证。
- `vendored/` 下的 skill 由 `sync-vendored-skills.sh` 从外部源同步，不应手动修改。

## 安装

```bash
git clone <repo> && cd my-agent-skill && ./install.sh
```

脚本会将 `skills/` 下所有 skill 符号链接到 `~/.claude/skills/` 和 `~/.codex/skills/`（如果 `~/.codex/` 存在）。

## Domain 说明

| Domain | 用途 |
| --- | --- |
| `design` | UI/UX 设计、视觉风格 |
| `workflow` | 开发流程辅助：方案设计、代码审查、debug、决策压测 |
| `harness` | 本机环境维护：Codex/MCP 健康检查、系统优化、worktree 管理 |
| `research-docs` | 调研、学习、文档生成、报告、会话管理 |
| `vendored` | 从外部仓库同步的第三方 skill 集合 |
