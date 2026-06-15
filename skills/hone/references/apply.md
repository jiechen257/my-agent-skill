# Apply Playbook

Apply materializes a Practice Brief into a local agent harness asset. It is the only stage allowed to modify real harness files, and only after explicit confirmation.

## Supported Assets

| Asset | Draft template | Default real target |
| --- | --- | --- |
| skill | `skill-draft.md` | `~/.codex/skills/<name>/SKILL.md` |
| rule | `rule-draft.md` | `~/.codex/AGENTS.md` or project `AGENTS.md` |
| hook | `hook-draft.md` | draft only unless explicitly installed |
| MCP config | `mcp-config-draft.md` | config fragment only unless explicitly applied |

Codex is the default target. Claude writes require explicit user request.

## Boundary

Always follow:

```text
Draft -> Stage -> Apply
```

### Draft

- Generate the artifact under `~/work-pro/agent-space/hone/asset-drafts/`.
- Do not change `~/.codex`, `~/.claude`, project files, or registry source paths.
- Include intended target and verification notes in the draft.

### Stage

- Show target path.
- State whether the target exists.
- Summarize overwrite/merge behavior.
- Show a diff or concise change summary when editing existing files.
- Wait for explicit confirmation.

### Apply

- Perform the write.
- Preserve unrelated user changes.
- Run lightweight validation.
- Report applied path, validation result, test prompt/command, and residual risk.

## Validation

After a real write:

- skill: check directory, `SKILL.md`, frontmatter, referenced files, and give a test prompt.
- rule: check target file, conflict risk, and scope.
- hook: check shebang, permissions, risky commands, and provide dry-run command.
- MCP config: check JSON/TOML syntax and target path; never write secrets.

## Self-Update

Hone may draft improvements to itself, but must not modify or install itself without explicit confirmation. Self-updates use the same Draft -> Stage -> Apply boundary.
