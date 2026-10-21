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
│   ├── codex-global.md    # 全局 Codex AGENTS.md 源文件（手动部署）
│   ├── claude-global.md   # Claude Code 全局规则源
│   ├── gemini-global.md   # Gemini CLI 全局规则源
│   └── opencode-global.md # OpenCode 全局规则源
├── scripts/
│   ├── audit-global-skills.sh
│   └── sync-vendored-skills.sh
├── skills/
│   ├── finance/           # Finance Skills 本地兼容 wrapper
│   ├── mattpocock/         # active Matt Pocock engineering/productivity wrapper
│   ├── harness/           # active agent / MCP 健康检查
│   ├── research-docs/     # active 报告和研究沉淀辅助
│   └── writing/           # active 写作编辑辅助
├── vendor/
│   └── skills/            # 外部同步源快照（mattpocock、leonsong09 等）
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
- `rules/` 存放各客户端全局规则源文件，手动部署到目标位置；用 `~/.agents/rules-sync/check-drift.sh` 检查源与实际副本。
- `scripts/audit-global-skills.sh` 检查 registry 安装、全局失效链接、Codex 个人/共享入口的重复名称，并从安装入口读取正文及递归引用的资源。
- wrapper 统一通过目录内隐藏的 `.upstream/` 相对软链接访问上游，避免 Codex 把上游正文重复发现为独立 skill：正文为 `.upstream/SKILL.md`，上游资源相对于 `.upstream/`，本地覆盖文件相对于 wrapper。传给文件工具时保留完整安装路径；需要规范路径时先解析软链接，避免手动化简 `../../../vendor/...`。
- domain 只表达稳定分类，避免把临时项目名放到 domain 层。
- skill 文件里不写密钥、token、机器专属凭证。
- `vendor/skills/` 下的源快照由 `sync-vendored-skills.sh` 从外部源同步，不应手动修改。
- `install.sh` 只安装 `registry/skills.yaml` 中 `codex: true` / `claude: true` 的 active skill；`codex: false` 且 `claude: false` 的 source snapshot 只用于同步。
- 通用工程 workflow 默认使用 Matt Pocock skills；Trellis 只作为 start / continue / finish 上下文记录层。
- Codex 的低频专用 skill 保留 `$skill-name` 手动调用，关闭自动匹配；停用的 skill 保留源码但不安装。具体名单见 [Skill 使用指南](docs/skill-usage-whitepaper.md)。

## 安装

```bash
git clone <repo> && cd my-agent-skill && ./install.sh
```

脚本会将 `registry/skills.yaml` 中的 active skill 符号链接到 `~/.claude/skills/` 和 `~/.codex/skills/`（如果 `~/.codex/` 存在），并清理指向本仓库但已不在 active registry 中的旧链接。

安装或修改 wrapper 后运行：

```bash
./scripts/audit-global-skills.sh
python3 -m unittest discover -s scripts/tests -v
```

解析器依赖声明在 `scripts/requirements-audit.txt`。当前 Python 未安装时，可用 `uv run --with-requirements scripts/requirements-audit.txt ./scripts/audit-global-skills.sh` 隔离运行审计；测试同样可通过 `uv run --with-requirements scripts/requirements-audit.txt python -m unittest discover -s scripts/tests -v` 运行。

引用检查也可单独运行 `python3 scripts/audit-skill-references.py`，默认递归发现 `~/.codex/skills/` 和 `~/.agents/skills/` 下的入口，跳过隐藏目录（包括 `.upstream/`），并按真实目录防止软链接循环。缺失的默认目录会跳过，显式 `--root` 指定的目录缺失仍报错；可用 `--entry` 单独验证一个入口。

可见软链接的断链在任意深度都会导致审计失败，包括未被正文直接引用的嵌套链接。隐藏目录仍不参与发现；wrapper 正文显式引用的 `.upstream/` 则通过引用链检查。

检查使用 `markdown-it-py` 的 CommonMark 规则识别链接，再实际打开正文及递归依赖；支持标题、括号文件名，以及完整／折叠／简写引用式写法。行内 `scripts/...`、`references/...` 等资源路径相对于文档所属的最近一个真实 `SKILL.md` 目录，Markdown 链接和显式 `./`、`../` 则相对于当前文档。忽略代码块示例、URL、占位符和行内输出目录。它验证文件可读性，不执行资源脚本，也不代表业务流程通过；诊断行号定位到链接所在的段落或列表项首行。

行内代码中的资源路径按字面文件名读取，保留 `%`、`#`、`?`、`=` 等字符；含空白的行内命令示例不作为资源路径。只有 Markdown 链接按 URI 规则去除查询和片段并解码一次，再识别 `<name>`、`{name}`、`${name}` 占位符及 `*` 通配模式。文件级软链接的相对引用保留其逻辑所在目录，去重同时考虑真实文件、所属 skill、相对引用基准和是否按 Markdown 解析，因此不同别名不会相互漏查。

安装后无需按项目切换 profile：

- 简单任务直接 Inline。
- 需求澄清、PRD、实现、TDD、bug 诊断、review、架构梳理走 `skills/mattpocock/*` wrapper。
- 有 `.trellis/workflow.md` 的项目只用 `trellis-start`、`trellis-continue`、`trellis-finish-work` 记录上下文。

## Domain 说明

| Domain | 用途 |
| --- | --- |
| `finance` | 金融分析、数据读取和可视化 wrapper，安装说明见 [Finance Skills](docs/finance-skills-installation.md) |
| `mattpocock` | Matt Pocock engineering/productivity wrapper |
| `harness` | 本地维护的 agent / MCP 健康检查 |
| `research-docs` | 本地维护的报告和研究沉淀辅助 |
| `writing` | 本地维护的写作编辑辅助 |
| `vendor/skills` | 从外部仓库同步的第三方 skill 源快照，不直接安装 |
