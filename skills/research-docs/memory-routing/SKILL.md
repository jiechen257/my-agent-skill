---
name: memory-routing
description: Use when deciding where to store, retrieve, or summarize durable knowledge for this user across Codex memories, Basic Memory MCP, repo docs, DingTalk/Yuque, daily reports, or project notes.
---

# Memory Routing

Choose the right persistence target before writing knowledge. The goal is to keep durable memory useful, source-faithful, and secret-safe.

## Scope

Use this skill when the user asks to:

- 转存 memory, 更新长期记忆, 保存经验, 写入知识库
- summarize a session, project, research thread, or debugging lesson
- decide whether a note belongs in Codex memory, Basic Memory, repo docs, DingTalk/Yuque, or daily reports
- retrieve prior context without mixing stale memory with current repo evidence

Do not write secrets, tokens, cookies, internal credentials, or raw sensitive logs into durable memory.

## Routing Rules

- **Codex native memories**: use for agent behavior preferences, recurring repo facts, and cross-session reminders. Update only when the user explicitly asks to update memory.
- **Basic Memory MCP / `agent-memory`**: use for durable personal knowledge, research notes, reusable technical findings, and distributed long-term memory. Redact secrets before writing.
- **Repo docs / `AGENTS.md`**: use for project-specific runtime rules, build/test commands, module boundaries, and conventions that should govern future agents in that repo.
- **Trellis `.trellis/spec/`**: use for executable project contracts, quality gates, workflow state, and implementation-relevant decisions in Trellis projects.
- **DingTalk / Yuque**: use for team-facing or organization-facing documents, meeting notes, OKR docs, shared requirements, and internal knowledge that should live in the company doc system.
- **Daily / weekly report repo**: use for work reports derived from commits, Codex sessions, and approved supplementary materials.
- **Session handoff**: use for immediate continuation context when the next agent needs exact state, commands, files, blockers, and acceptance criteria.

## Workflow

```text
[1] Classify the knowledge
      -> preference, repo rule, research result, team doc, work report, or handoff

[2] Check sensitivity
      -> redact credentials and private raw logs before persistence

[3] Choose one primary target
      -> avoid writing the same fact into multiple stores unless each target has a distinct audience

[4] Preserve source anchors
      -> include file paths, commit hashes, doc links, command outputs, or dates when useful

[5] Report what was written
      -> target, note title/path, and any redaction decisions
```

## Rules

- Prefer current repo evidence over older memory when facts may drift.
- Treat memory as a starting point, not proof, for code architecture or live environment state.
- Keep user-facing wording concise and actionable.
- For Basic Memory writes, use the available Basic Memory MCP path when present.
- For Codex memory updates, follow the active session memory-update rules rather than editing memory files directly.

## Verification

Minimum completion evidence:

- state the chosen persistence target
- state why that target fits the audience and reuse pattern
- include the written artifact path, document URL, or MCP write result when a write happened
