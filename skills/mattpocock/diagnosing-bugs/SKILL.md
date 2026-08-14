---
name: diagnosing-bugs
description: "Diagnose bugs, regressions, failing tests, or performance issues; trigger when a problem persists after a fix, moves to another path, or follow-up feedback invalidates earlier assumptions."
---

# Diagnosing Bugs

Read `../../../vendor/skills/mattpocock/diagnosing-bugs/SKILL.md` relative to this file completely and follow it, with the local continuity rules below taking precedence.

Resolve relative references, scripts, or assets from `../../../vendor/skills/mattpocock/diagnosing-bugs/`.

## Incident continuity

Treat repeated reports on the same theme as one incident. Before building the vendor feedback loop, reconstruct its lineage:

1. Record the original symptom and expected behavior.
2. Record each attempted fix, its evidence, and what changed afterward.
3. Mark which assumptions later feedback confirmed or invalidated.
4. List every original and follow-up symptom that one causal model must explain.

The feedback loop must detect the original problem and the relevant follow-up symptoms. A loop that covers only the newest manifestation is incomplete.

When a problem remains after a fix, appears in an equivalent caller or consumer, or moves to another state or platform, pause local patching and return to root-cause diagnosis. The accepted cause must explain both the symptoms and why the earlier fix failed or displaced them. If it cannot, report the causal model as unresolved instead of applying another symptom-level patch.
