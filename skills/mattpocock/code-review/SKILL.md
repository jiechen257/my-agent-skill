---
name: code-review
description: "Review branch, PR, or work-in-progress changes against repo standards, the original problem, and constraints accumulated through follow-up requests."
---

# Code Review

Read `../../../vendor/skills/mattpocock/code-review/SKILL.md` relative to this file completely and follow it, with the local continuity rules below taking precedence.

Resolve relative references, scripts, or assets from `../../../vendor/skills/mattpocock/code-review/`.

## Continuity review

Treat the task conversation as part of the originating spec. Before judging the diff, reconstruct:

- the original user-visible problem and expected outcome;
- constraints, corrections, and non-regressions added by every relevant follow-up;
- previous implementations or review fixes and their observed results;
- the incremental question posed by the latest review request.

Apply the vendor Standards and Spec axes to that accumulated context, then make a continuity pass:

1. Does the implementation address the original problem at the verified requirement or causal boundary?
2. Does it preserve every still-valid constraint from earlier follow-ups?
3. Were equivalent callers, consumers, states, platforms, and failure paths affected by the same cause examined?
4. Did the change solve the problem, or only move its symptom to an adjacent path?

On a repeated review, classify each genuinely new finding as introduced by a later fix, exposed by new evidence or scope, or missed by the previous review. A previous miss is a signal to expand the current analysis before reporting, not an excuse to reset the review around the latest query.

A review cannot pass unless its conclusion explains how the implementation serves the original problem and each relevant follow-up. State unresolved context or causal uncertainty explicitly.
