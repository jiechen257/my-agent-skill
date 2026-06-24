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
├── plugins/
│   └── ponytail/          # vendored agent plugin（Codex 插件结构）
├── scripts/
│   ├── audit-global-skills.sh
│   └── sync-vendored-skills.sh
├── skills/
│   ├── design/            # active skill wrapper 和本地设计辅助
│   ├── workflow/           # active workflow router 和本地开发流程辅助
│   ├── harness/           # active agent / MCP 健康检查
│   ├── research-docs/     # active 调研、文档、报告辅助
│   └── superpowers/       # explicit-only Superpowers wrapper
├── vendor/
│   └── skills/            # 外部同步源快照（Waza、superpowers、leonsong09 等）
├── prompts/
│   └── best-prompts/      # 个人收藏的 prompt 模板（不参与自动化，手动引用）
└── templates/
    ├── SKILL.template.md
    └── SKILL.with-references.template.md
```

## 约定

- 真实会被安装和自动发现的 active skill 只放在 `skills/` 下。
- 每个 skill 使用独立目录：`skills/<domain>/<skill-name>/`。
- 每个 skill 必须包含一个 `SKILL.md`，可按需附带 `agents/`、`references/`、`scripts/`、`assets/`。
- `vendor/skills/` 只存上游同步源快照，不直接安装，不作为默认自动发现面。
- `templates/` 只放可复用骨架，不作为 active skill。
- `prompts/` 存放个人收藏的 prompt 模板，供手动复制使用，不参与 install 或 registry。
- `plugins/` 存放完整 agent plugin 收录件，保留上游插件结构，不参与 skill 安装脚本。
- `rules/` 存放全局 agent 规则源文件，手动部署到目标位置（如 `~/.codex/AGENTS.md`）。
- domain 只表达稳定分类，避免把临时项目名放到 domain 层。
- skill 文件里不写密钥、token、机器专属凭证。
- `vendor/skills/` 下的源快照由 `sync-vendored-skills.sh` 从外部源同步，不应手动修改。
- `install.sh` 只安装 `registry/skills.yaml` 中 `codex: true` / `claude: true` 的 active skill；`codex: false` 且 `claude: false` 的 source snapshot 只用于同步。
- Waza / Trellis / Superpowers 的 workflow 冲突由 `rules/codex-global.md` 和 `skills/workflow/*` router 处理，不靠切换全局 profile。

## 安装

```bash
git clone <repo> && cd my-agent-skill && ./install.sh
```

脚本会将 `registry/skills.yaml` 中的 active skill 符号链接到 `~/.claude/skills/` 和 `~/.codex/skills/`（如果 `~/.codex/` 存在），并清理指向本仓库但已不在 active registry 中的旧链接。

安装后无需按项目切换 profile：

- 有 `.trellis/workflow.md` 的项目：`think` / `check` / `hunt` wrapper 会把 workflow owner 交给 Trellis。
- 没有 `.trellis/workflow.md` 的项目：`think` / `check` / `hunt` wrapper 会读取 Waza 源并按 Waza 工作流执行。
- Superpowers wrapper 只在用户显式点名对应 skill 时触发；普通任务中可被 Trellis / Waza 作为参考材料读取，但不成为 workflow owner。

## Domain 说明

| Domain | 用途 |
| --- | --- |
| `design` | 本地维护的 UI/UX 设计辅助 |
| `workflow` | 本地维护的开发流程辅助 |
| `harness` | 本地维护的 agent / MCP 健康检查 |
| `research-docs` | 本地维护的调研、文档、报告辅助 |
| `superpowers` | 显式点名才使用的 Superpowers wrapper |
| `vendor/skills` | 从外部仓库同步的第三方 skill 源快照，不直接安装 |
