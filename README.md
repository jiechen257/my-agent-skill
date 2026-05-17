# my-agent-skill

这个仓库集中存放个人 Codex / Agent skills，采用分域目录组织，便于同步、检索和接入不同 Agent 工具。

## 目录结构

```text
my-agent-skill/
├── .agent/
│   └── skills/        # Copilot CLI / Agent 风格的扁平 skill 入口
├── .agents/
│   └── skills/        # Trellis / 多 Agent 兼容入口，可作为占位目录
├── .claude/
│   └── skills/        # Claude Code 风格的扁平 skill 入口
├── README.md
├── AGENTS.md
├── AGENTS.trellis.md
├── skills/
│   ├── automation/
│   ├── content/
│   ├── design/
│   ├── development/
│   └── research/
│       └── <skill-name>/
│           ├── SKILL.md
│           ├── agents/       (可选)
│           ├── references/   (可选)
│           ├── scripts/      (可选)
│           └── assets/       (可选)
└── templates/
    ├── SKILL.template.md
    └── SKILL.with-references.template.md
```

## 约定

- `AGENTS.trellis.md` 保存本机 Codex 全局 Trellis 规则快照，避免覆盖仓库自身的 `AGENTS.md`。
- 真实可用的 skill 只放在 `skills/` 下。
- 每个 skill 使用独立目录：`skills/<domain>/<skill-name>/`。
- 每个 skill 必须包含一个 `SKILL.md`，可按需附带 `agents/`、`references/`、`scripts/`、`assets/`。
- `templates/` 只放可复用骨架，不作为 active skill。
- domain 只表达稳定分类，避免把临时项目名放到 domain 层。
- skill 文件里不写密钥、token、机器专属凭证。
- 部分 vendored skill 保留上游 `README.md`、`LICENSE` 或 `.gitignore`，这些文件不影响 Agent 发现 `SKILL.md`。

## Skills

### Automation

重复性 shell 工作流、会话收尾、日报、交接和跨会话整理。

| Skill | 用途 |
| --- | --- |
| [`commit-daily-summary`](skills/automation/commit-daily-summary/SKILL.md) | 基于当天 git commits 生成中文提交总结或日报。 |
| [`project-daily-summary`](skills/automation/project-daily-summary/SKILL.md) | 汇总当天 Codex 会话、提交和未提交改动，按项目输出工作日报。 |
| [`session-handoff`](skills/automation/session-handoff/SKILL.md) | 生成可交给新 Agent 继续工作的完整 handoff prompt。 |
| [`session-wrap`](skills/automation/session-wrap/SKILL.md) | 收尾当前 coding session，整理完成项、遗留问题和后续建议。 |
| [`weekly-report-template`](skills/automation/weekly-report-template/SKILL.md) | 按指定仓库和日期范围，从 git 记录生成周报。 |
| [`worktree-closeout`](skills/automation/worktree-closeout/SKILL.md) | 只读扫描多 worktree / branch 收口状态，输出合并与清理建议。 |

### Development

Trellis 管理的开发流程、任务状态、项目规范注入和质量门禁。

| Skill | 用途 |
| --- | --- |
| [`trellis-start`](skills/development/trellis-start/SKILL.md) | 启动 Trellis session，加载当前任务、工作流、git 状态和项目规范。 |
| [`trellis-continue`](skills/development/trellis-continue/SKILL.md) | 继续 Trellis 当前任务，按 workflow phase 定位下一步。 |
| [`trellis-brainstorm`](skills/development/trellis-brainstorm/SKILL.md) | 在实现前做需求发现、PRD 梳理、MVP 收敛和任务创建。 |
| [`trellis-before-dev`](skills/development/trellis-before-dev/SKILL.md) | 写代码前读取 `.trellis/spec/` 中适用的项目规范和 checklist。 |
| [`trellis-check`](skills/development/trellis-check/SKILL.md) | 完成代码后做 spec compliance、lint、type-check、tests 和跨层检查。 |
| [`trellis-break-loop`](skills/development/trellis-break-loop/SKILL.md) | bug 修复后分析根因、失败原因和预防机制，沉淀可复用经验。 |
| [`trellis-update-spec`](skills/development/trellis-update-spec/SKILL.md) | 将调试、实现或讨论中获得的规范与契约写回 `.trellis/spec/`。 |
| [`trellis-finish-work`](skills/development/trellis-finish-work/SKILL.md) | 结束 Trellis 任务，校验提交状态、归档任务并记录 session journal。 |
| [`trellis-meta`](skills/development/trellis-meta/SKILL.md) | 理解和定制项目内 Trellis 架构、平台文件、hooks、skills 和 workflow。 |

### Content

内容生成、图形输出和可交付制品。

| Skill | 用途 |
| --- | --- |
| [`architecture-diagram`](skills/content/architecture-diagram/SKILL.md) | 生成架构图、流程图、数据流、时序图、状态机等 standalone SVG 技术图。 |

### Design

产品界面风格、视觉系统和前端实现约束。

| Skill | 用途 |
| --- | --- |
| [`colawd-ui-style`](skills/design/colawd-ui-style/SKILL.md) | 复刻 colawd 风格工作台 UI：黑色 terminal shell、浅黄网格、粗边框和高饱和状态色。 |

### Research

调研整理、分析纪要和知识库沉淀。

| Skill | 用途 |
| --- | --- |
| [`research-note-wrap`](skills/research/research-note-wrap/SKILL.md) | 将当前会话或当天相关会话整理成可读的 Obsidian 中文研究笔记。 |

## Agent 集成

本仓库采用“真实内容 + 平台入口”的结构：`skills/` 保存真实可维护内容，隐藏目录负责把这些 skill 暴露给不同 Agent 工具。

| 目录 | 作用 | 内容形态 |
| --- | --- | --- |
| `skills/` | 真实 skill 源目录，按 domain 分组维护 | 实际 `SKILL.md`、`references/`、`scripts/`、`assets/` |
| `.claude/skills/` | Claude Code 风格入口 | 扁平 symlink，指向 `skills/<domain>/<skill-name>` |
| `.agent/skills/` | Copilot CLI / Agent 风格入口 | 扁平 symlink，指向 `skills/<domain>/<skill-name>` |
| `.agents/skills/` | Trellis / 多 Agent 兼容入口 | 可放 Trellis skill 入口或占位目录，按项目工具链需要启用 |

Copilot CLI 风格的 `.agent/` 与 Claude Code 风格的 `.claude/` 都使用扁平 symlink 接入 skill。每个 Agent 只发现一层目录：

```text
.agent/skills/
└── <skill-name> -> ../../skills/<domain>/<skill-name>
.claude/skills/
└── <skill-name> -> ../../skills/<domain>/<skill-name>
```

保持 Agent 入口为扁平结构。嵌套 domain 会导致部分 Agent 无法发现 `SKILL.md`。

## 新增 Skill

1. 选择稳定 domain，例如 `automation`、`development`、`research`、`content`、`design`。
2. 创建目录：`skills/<domain>/<skill-name>/`。
3. 复制模板：`templates/SKILL.template.md` 或 `templates/SKILL.with-references.template.md` 到新目录并命名为 `SKILL.md`。
4. 填写 frontmatter 的 `name` 和 `description`，正文保持短而可执行。
5. 只有在能明显提高复用性时，才新增 `references/`、`scripts/`、`assets/`。
6. 在本 README 的对应 domain 表格里添加一行。
7. 创建扁平 symlink：

```bash
ln -sf ../../skills/<domain>/<skill-name> .agent/skills/<skill-name>
ln -sf ../../skills/<domain>/<skill-name> .claude/skills/<skill-name>
```

## 命名建议

- 目录名使用小写 kebab-case。
- `name` 保持稳定、清晰、可触发。
- 名称优先表达对象和动作，例如 `session-handoff`、`trellis-update-spec`、`worktree-closeout`。
- 分类不够确定时，优先放到最贴近触发场景的 domain，再在 README 里写清用途。

## 来源

- `session-handoff`：<https://github.com/Innei/SKILL/tree/main/skills/automation/session-handoff>
- Trellis 系列：来自本机 `/Users/jiechen/per-pro/personal-kb/.agents/skills/trellis-*`
- `research-note-wrap`：<https://github.com/leonsong09/research-note-wrap>
- `session-wrap`：<https://github.com/leonsong09/session-wrap>
- `commit-daily-summary`：<https://github.com/leonsong09/commit-daily-summary>
- `project-daily-summary`：<https://github.com/leonsong09/project-daily-summary>
- `worktree-closeout`：<https://github.com/leonsong09/worktree-closeout>

`session-handoff` 已同时安装到全局 Codex skills 目录：`/Users/jiechen/.codex/skills/session-handoff`。重启 Codex 后可被全局 skill 索引发现。
