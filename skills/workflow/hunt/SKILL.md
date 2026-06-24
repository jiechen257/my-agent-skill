---
name: hunt
description: "Use when users report errors, crashes, regressions, failing tests, broken behavior, screenshot evidence, or something that used to work and now fails."
---

# Hunt Router

Before using any debugging workflow, check the current project root for `.trellis/workflow.md`.

- If `.trellis/workflow.md` exists, Trellis is the workflow owner. Use the project's Trellis debugging or break-loop flow. Do not invoke Waza `hunt` or Superpowers debugging workflow as independent workflow owners.
- If `.trellis/workflow.md` does not exist, read `../../../vendor/skills/waza/hunt/SKILL.md` relative to this file and follow it. Resolve its relative files from `../../../vendor/skills/waza/hunt/`.

Superpowers debugging files may be read as reference material only when explicitly needed; they must not own the diagnosis or verification path for this route.
