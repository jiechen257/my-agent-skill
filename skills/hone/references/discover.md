# Discover Playbook

Discover finds frontier signals that may affect the user's local agent harness. It is a radar, not a long research report.

## Defaults

```text
time window: 7d
sources: GitHub Trending, Hacker News, Reddit, linux.do, Product Hunt
output: Top 8
focus: agent skill, MCP, hooks, local harness, AI coding workflow, Codex Desktop, Claude Code
depth: light scan
```

Run deeper research only when the user says `deep`, `深挖`, `展开`, or asks for a specific candidate.

## Source Policy

Use public sources only unless the user explicitly approves logged-in browsing.

| Source | Role | Confidence |
| --- | --- | --- |
| GitHub Trending/search/repos | tools, repos, MCP servers, frameworks | maintainer or community |
| Hacker News | technical discussion and release signals | community |
| Reddit | user pain, workaround, adoption and failure cases | community |
| linux.do | Chinese community practice signals | community |
| Product Hunt | product/tool radar and interaction patterns | community |

Product Hunt is not engineering proof. Treat it as product radar unless backed by maintainer or official evidence.

## Evidence Rules

- Every Top 8 candidate must have a URL.
- Every candidate must include `sourceTier` and `confidence`.
- `confirmed` is allowed only for official sources.
- Community sources default to `community_reported` or `unverified`.
- No URL means the item can be a temporary observation, not a formal candidate.

## Ranking

Rank by local practice value, not raw popularity:

1. local harness impact: affects skill, rule, hook, MCP, Codex workflow, Claude workflow
2. actionability: can become a Practice Brief or asset draft
3. evidence quality: official/maintainer/high-quality discussion
4. novelty: new method, tool, pain, or workflow pattern
5. heat: stars, comments, upvotes, rank

## Output

Default output is a short list grouped by action:

```text
建议 shape
建议 deep read
建议 watch
建议 ignore
```

Each item shows only: title, source URL, source tier/confidence, why it matters, recommended action.

Use the full candidate schema in [output formats](output-formats.md) only when saving a scout report or doing deeper research.
