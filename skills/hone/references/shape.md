# Shape Playbook

Shape turns one or more signals into a Practice Brief. A Practice Brief is a decision artifact for applying a practice, not a product data card.

## Inputs

Accept any of:

- a candidate number from the current discover result
- a URL or pasted source text
- a short idea from the user
- a saved scout report path

If the input is ambiguous and no current candidate exists, ask one concise question.

## Output

Produce the brief in the conversation by default. Save it only when the user asks.

Use [practice-brief.md](../templates/practice-brief.md) when saving.

## Practice Brief Requirements

Every brief must answer:

- Is this worth adopting?
- Where does it fit in the local agent harness?
- What should change: skill, rule, hook, MCP config, or workflow?
- What evidence supports it?
- What is the risk or non-fit case?
- What would `apply` draft first?

## Decision Rules

- Recommend `skill` for reusable workflows, review protocols, research flows, or debugging methods.
- Recommend `rule` for stable behavior constraints and preferences.
- Recommend `hook` for repeatable checks or automation boundaries; draft only unless explicitly installed.
- Recommend `MCP config` for tool or data-source connections; never include secrets.
- If the source evidence is weak, recommend `watch` or `deep read` instead of `apply`.

## Save Path

When asked to save:

```text
~/work-pro/agent-space/hone/practice-briefs/YYYY-MM-DD-<slug>.md
```

Do not save every brief automatically.
