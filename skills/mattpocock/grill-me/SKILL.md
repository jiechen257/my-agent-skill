---
name: grill-me
description: "Relentlessly stress-test an existing plan, PRD, design, or Trellis planning artifact before implementation. Use when the user asks to be grilled or when a Trellis plan needs a final adversarial review."
---

# Grill Me

Stress-test an existing plan. Do not replace brainstorming and do not start implementation.

## 1. Load the plan

Read the current PRD, design, implementation plan, acceptance criteria, and relevant code/spec evidence. In a Trellis project, use the active task artifacts as the source of truth.

Completion criterion: the stated goal, scope, proposed behavior, constraints, and validation approach are all explicit enough to attack.

## 2. Build the attack map

Challenge every material branch:

- Goal and non-goals
- User-visible states and failure behavior
- Contracts, data flow, compatibility, migration, and rollback
- Security, privacy, performance, observability, and operational risk
- Test seams, acceptance evidence, and missing integration touch points

Derive answers from the repo before asking the user. Separate facts, assumptions, and decisions.

Completion criterion: every high-impact assumption is either supported by evidence or recorded as an unresolved decision.

## 3. Grill one decision at a time

Ask only the highest-risk unresolved question. Give a recommended answer and concrete trade-offs. After each answer, update the planning artifact before moving to the next question.

Do not reopen settled decisions without new evidence. Do not turn the review into a second planning workflow.

Completion criterion: no unresolved decision can materially change scope, public behavior, architecture, or acceptance criteria.

## 4. Close the review gate

Return:

- Decisions changed or confirmed
- Risks accepted or mitigated
- Remaining non-blocking unknowns
- Whether the plan is ready for implementation

In Trellis, implementation may start only after blocking findings are reflected in task artifacts and the user confirms the revised plan.
