---
name: hone
description: Use when the user mentions hone or asks about frontier AI coding signals, local agent harness practices, Codex skills/rules/hooks/MCP config, or Codex/Claude harness drift.
---

# Hone

Hone is a Codex Desktop-first skill for maintaining a local agent harness. It replaces the old app-shaped workflow with one conversational entrypoint and four internal stages:

```text
discover -> shape -> apply -> check
```

Default to Simplified Chinese unless the user asks otherwise.

## Routing

Use the stable anchors when present:

| User intent | Route |
| --- | --- |
| `hone`, `hone discover`, `发现`, `扫一下`, `有什么值得看` | [discover](references/discover.md) |
| `shape`, `整理`, `转成实践`, `分析这条` | [shape](references/shape.md) |
| `apply`, `应用`, `写成 skill`, `生成草稿`, `安装` | [apply](references/apply.md) |
| `check`, `检查`, `审计`, `drift`, `本地 harness` | [check](references/check.md) |

If the user only says `hone`, run `discover` with defaults. If the current conversation already contains selected candidates, briefs, drafts, or findings, route directly to the stage implied by the user.

## Defaults

- `discover`: public web search, last 7 days, GitHub Trending, Hacker News, Reddit, linux.do, Product Hunt, Top 8 short list.
- `shape`: produce a Practice Brief in the conversation; save only when asked.
- `apply`: create an asset draft by default; real writes require explicit confirmation.
- `check`: scan only high-value Codex, Claude, and registry harness entrypoints; no logs, secrets, or full source trees by default.

## State Model

Do not use a database. Keep transient state in the current conversation. Save only reusable artifacts:

```text
~/work-pro/agent-space/hone/
  scout-reports/
  practice-briefs/
  asset-drafts/
  check-reports/
```

Automatically save `apply` drafts. Save discover reports, Practice Briefs, and check reports only when the user asks.

## Write Boundary

All modifications to real agent harness locations use the same boundary:

```text
Draft -> Stage -> Apply
```

- Draft: write only to `~/work-pro/agent-space/hone/asset-drafts/`.
- Stage: show target path, overwrite behavior, and diff or summary; still no real write.
- Apply: write only after explicit user confirmation, then run lightweight validation.

Default write target is Codex. Claude is read-only unless the user explicitly asks to write Claude assets.

See [safety boundaries](references/safety-boundaries.md) before any real write.

## Internal Playbooks

Read the relevant playbook before acting:

- [discover](references/discover.md)
- [shape](references/shape.md)
- [apply](references/apply.md)
- [check](references/check.md)
- [output formats](references/output-formats.md)
- [safety boundaries](references/safety-boundaries.md)

Use templates from `templates/` when creating saved artifacts.

## Completion Contract

Every run should end with the smallest useful next action:

- after `discover`: `shape 第 N 条`, `展开第 N 条`, or `保存报告`
- after `shape`: `apply 成草稿`, `保存 brief`, or `放弃`
- after `apply`: written draft path or applied path, validation result, and a test prompt/command
- after `check`: fix queue and which finding can be handed to `apply`
