# Check Playbook

Check inspects the local agent harness and returns a fix queue. It diagnoses by default; it does not fix by default.

## Default Scope

Read-only:

```text
~/.codex/skills/
~/.codex/AGENTS.md
~/.codex/config.toml
~/.claude/skills/
~/.claude/CLAUDE.md
~/.claude/settings.json
~/work-pro/my-agent-skill/skills/
~/work-pro/my-agent-skill/AGENTS.md
```

Only inspect project-level files such as cwd `AGENTS.md`, `CLAUDE.md`, `.trellis`, or package scripts when the user explicitly asks for project check.

## Exclusions

Do not read by default:

- complete logs
- secrets or tokens
- browser data
- full project source trees
- historical chat transcripts

## Finding Types

Use these buckets:

- duplicate: equivalent skills/rules exist in multiple places
- drift: registry and installed target differ
- missing: expected target or reference is absent
- broken: referenced file/template/path does not exist
- stale: old behavior or obsolete workflow appears likely
- risk: hook/MCP/config has unsafe or unclear boundary
- improve: low-risk quality improvement

## Fix Queue

Group findings:

```text
可直接修复
需要判断
仅观察
```

When the user chooses a finding, hand it to `apply` as a draft or staged change. Do not directly repair from `check`.

## Output

Default to a concise top findings report. Save to `~/work-pro/agent-space/hone/check-reports/` only when the user asks.
