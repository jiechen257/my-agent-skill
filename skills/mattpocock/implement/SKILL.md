---
name: implement
description: "Implement work from a PRD, issue, or agreed scope while preserving the original problem and accumulated follow-up constraints."
---

# Implement

Read `../../../vendor/skills/mattpocock/implement/SKILL.md` relative to this file completely and follow it, with the local continuity rules below taking precedence.

Resolve relative references, scripts, or assets from `../../../vendor/skills/mattpocock/implement/`.

## Problem frame

Before editing, reconstruct the current problem from the full task conversation:

- the original user-visible outcome;
- constraints, corrections, and non-regressions accumulated through follow-ups;
- attempted approaches, observed results, confirmed facts, and invalidated assumptions;
- what the latest request adds to that existing context;
- the verified requirement or causal boundary and its affected callers, consumers, states, and failure paths.

A follow-up on the same theme updates this frame; it does not reset it. If the latest request conflicts with the original outcome or an earlier constraint, surface the conflict and resolve it before editing.

Analyze as broadly as needed to establish the whole problem. Keep writes tied to the verified boundary. Before implementation begins, be able to state why the proposed change addresses the original problem and all still-valid follow-ups instead of only the newest symptom.
