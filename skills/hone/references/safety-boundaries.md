# Safety Boundaries

Hone is execution-first but conservative around real harness changes.

## Allowed Without Confirmation

- Public web search and public page reading for `discover`.
- Reading default harness entrypoints for `check`.
- Producing conversation-only briefs and recommendations.
- Writing drafts under `~/work-pro/agent-space/hone/asset-drafts/`.

## Requires Confirmation

- Writing to `~/.codex/skills`, `~/.codex/AGENTS.md`, or `~/.codex/config.toml`.
- Writing to any `~/.claude` file or directory.
- Editing project `AGENTS.md`, `CLAUDE.md`, hooks, MCP config, or task files.
- Installing or enabling hooks.
- Applying MCP config.
- Modifying Hone's own source or installed skill.

## High-Risk Access

Ask before:

- logged-in browsing
- reading complete logs
- reading secrets, tokens, cookies, or private credentials
- deep scanning project source trees
- deleting, archiving, or replacing existing harness assets

## Source Confidence

- `official`: official docs, changelog, release notes, official repo. Can be `confirmed`.
- `maintainer`: project author repo, README, issue, discussion. Use `maintainer_claimed`.
- `community`: HN, Reddit, linux.do, Product Hunt, blog posts. Use `community_reported` or `unverified`.

Never present community reports as confirmed facts.
