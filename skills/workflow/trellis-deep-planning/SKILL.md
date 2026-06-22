---
name: trellis-deep-planning
description: |
  Use in Trellis projects when deep planning is needed before implementation.
  Reads Superpowers brainstorming/writing-plans as reference discipline when available,
  but keeps Trellis as the only workflow owner and writes only Trellis task artifacts.
  Do not trigger for ordinary feature requests.
---

# Trellis Deep Planning

Strengthen the current Trellis task before implementation.

Trellis remains the workflow owner. This skill may reference-read Superpowers planning skills, but it does not invoke their workflows.

## Trigger Check

Before running, verify:

1. The repo contains `.trellis/`.
2. There is a current or intended Trellis task.
3. The user explicitly requested deep planning / Superpowers-style planning, or the task meets Deep Planning Mode:
   - cross-module behavior change
   - shared logic
   - public API / schema
   - persistence
   - concurrency
   - complex UI flow
   - large refactor
   - unclear blast radius
4. Do not run alongside `trellis-brainstorm`.
5. Do not start full Superpowers workflow.

If the trigger is not satisfied, return to the normal Trellis route.

## Reference-Read Superpowers Planning Skills

When this skill runs, try to read these skills as reference material if available:

- `brainstorming`
- `writing-plans`

Prefer the current Codex skill list. If unavailable, try repo-local vendored paths:

- `skills/vendored/superpowers/brainstorming/SKILL.md`
- `skills/vendored/superpowers/writing-plans/SKILL.md`

If neither is available, continue with this skill's built-in discipline summary and report that the Superpowers references were unavailable.

Reading a reference skill is not invoking that skill. Do not announce that you are using `brainstorming` or `writing-plans`. Announce only `trellis-deep-planning` as the active skill.

Use Superpowers reference material only for planning discipline:

- context exploration
- one-question-at-a-time clarification
- 2-3 approach comparison
- recommendation with trade-offs
- sectioned design review when decisions materially affect implementation
- no-placeholder implementation planning
- exact files, interfaces, tests, commands, expected results
- self-review

Do not use Superpowers workflow ownership:

- do not invoke `brainstorming` as a workflow
- do not invoke `writing-plans` as the next skill
- do not write `docs/superpowers/specs/*`
- do not write `docs/superpowers/plans/*`
- do not commit planning docs unless the user explicitly asks
- do not transition to `executing-plans` or `subagent-driven-development`

## Required Inputs

Read before writing:

1. `.trellis/workflow.md`
2. current active task metadata under `.trellis/tasks/`
3. relevant `.trellis/spec/` files
4. related source files, tests, docs, and recent commits

## Planning Process

1. Explore project context first.
2. Clarify only high-value unknowns.
3. Ask at most one question at a time.
4. Prefer multiple-choice questions when possible.
5. Propose 2-3 approaches with trade-offs and a recommendation when there is a material design choice.
6. Present design sections for approval only when the decision materially affects implementation.
7. Update Trellis task artifacts until they are ready for implementation.
8. Do not implement code until task artifacts pass self-review.

## Approval Gates

Ask for user confirmation only when a decision materially changes implementation direction, scope, public behavior, data model, persistence, API/schema, or risk profile.

Do not stop for approval on:

- formatting the Trellis task artifacts
- filling missing acceptance criteria inferred from context
- splitting implementation tasks
- adding verification commands
- strengthening self-review details

Before handing back to implementation, state whether the task is ready for `trellis-continue`. If material assumptions remain unresolved, mark it not ready and ask one question.

## Artifact Policy

Work inside the current Trellis task.

Required outcome:

- `prd.md` is clear enough to define goal, non-goals, behavior, acceptance criteria, constraints, risks, and validation.
- `design.md` is clear enough to choose an approach and define boundaries, data flow, interfaces, error handling, tests, and risks.
- `implement.md` is concrete enough to execute with exact files, ordered tasks, interfaces/types, tests, commands, expected results, and rollback/risk notes.

Do not rewrite files that are already sufficient. Patch gaps. If `prd.md` is sufficient, focus on `design.md` and `implement.md`.

## Design Minimum Content

`design.md` must cover, when relevant:

- recommended approach
- alternatives considered
- architecture
- component boundaries
- data flow
- state model
- API / schema / type changes
- error handling
- migration / compatibility notes
- testing strategy
- open questions and resolved assumptions

## Implementation Plan Minimum Content

`implement.md` must include:

- exact file paths
- ordered tasks
- interfaces, types, functions, or schema changes
- test cases or test code
- verification commands and expected results
- rollback or risk-control notes when relevant

## Placeholder Ban

The plan fails if it contains:

- TBD
- TODO
- implement later
- fill in details
- add appropriate error handling
- add validation
- handle edge cases
- write tests for the above
- similar to previous task
- references to undefined types, functions, methods, files, fields, or schemas

## Self-Review Record

After updating task artifacts, append or update a short `Self-review` section in `implement.md`.

It must state:

- acceptance criteria coverage: covered / gaps
- design-to-file mapping: covered / gaps
- test and verification coverage: covered / gaps
- unresolved assumptions, if any
- readiness: ready for `trellis-continue` / not ready

Keep it brief. Fix gaps inline before marking ready.

## Handoff After Planning

After self-review:

- If the original user request asked only for planning / Deep Planning, stop and report readiness.
- If the original user request asked to plan and implement, and readiness is `ready`, return to the Trellis implementation route (`trellis-continue` or the project workflow's equivalent).
- If readiness is `not ready`, ask one blocking question and do not implement.

End by stating:

- which Trellis task files were created or updated
- whether Superpowers reference skills were read or unavailable
- the selected approach
- remaining assumptions
- whether the task is ready for `trellis-continue`
