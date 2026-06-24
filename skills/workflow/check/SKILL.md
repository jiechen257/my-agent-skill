---
name: check
description: "Use when users ask for code review, release gates, issue or PR triage, commit/push/publish readiness, or project quality audits."
---

# Check Router

Before using any review or release workflow, check the current project root for `.trellis/workflow.md`.

- If `.trellis/workflow.md` exists, Trellis is the workflow owner. Use the project's Trellis check, finish, and quality gate flow. Do not invoke Waza `check` or Superpowers review workflow as independent workflow owners.
- If `.trellis/workflow.md` does not exist, read `../../../vendor/skills/waza/check/SKILL.md` relative to this file and follow it. Resolve its relative files from `../../../vendor/skills/waza/check/`.

Superpowers review and verification files may be read as reference material only when explicitly needed; they must not replace the selected workflow owner.
