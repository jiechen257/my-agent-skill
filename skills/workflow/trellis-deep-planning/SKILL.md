---
name: trellis-deep-planning
description: |
  Use only when the project already has .trellis/ and the user explicitly asks for deep planning,
  Superpowers-style planning, stronger PRD/design/implement docs, or when the task clearly matches
  Deep Planning Mode from the global AGENTS.md. Do not trigger for ordinary feature requests.
---
# Trellis Deep Planning
You strengthen the current Trellis task before implementation.
## Trigger check
Before running, verify all conditions:
1. The repo contains `.trellis/`.
2. There is a current or intended Trellis task.
3. The user explicitly requested deep planning / Superpowers-style planning, or the task meets Deep Planning Mode:
   - new feature
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
6. Do not create `docs/superpowers/specs/*` unless the user explicitly asks for an external planning artifact.
If the trigger is not satisfied, return to the normal Trellis route.
## Role
Trellis is the workflow owner.
This skill only provides Superpowers-style planning discipline inside the Trellis task.
## Required inputs
Read before writing:
1. `.trellis/workflow.md`
2. current active task metadata under `.trellis/tasks/`
3. relevant `.trellis/spec/` files
4. related source files, tests, docs, and recent commits
## Planning process
1. Explore project context first.
2. Clarify only high-value unknowns.
3. Ask at most one question at a time.
4. Prefer multiple-choice questions when possible.
5. Propose 2-3 approaches with trade-offs and a recommendation.
6. Present the design in sections and ask for approval when the decision materially affects implementation.
7. Write or update:
   - `.trellis/tasks/<task>/prd.md`
   - `.trellis/tasks/<task>/design.md`
   - `.trellis/tasks/<task>/implement.md`
8. Do not implement code until these files pass self-review.
## PRD minimum content
`prd.md` must include:
- goal
- non-goals
- user-visible behavior
- acceptance criteria
- constraints
- risk areas
- validation requirements
## Design minimum content
`design.md` must include:
- recommended approach
- alternatives considered
- architecture
- component boundaries
- data flow
- state model, if relevant
- API / schema / type changes, if relevant
- error handling
- migration / compatibility notes, if relevant
- testing strategy
- open questions and resolved assumptions
## Implementation plan minimum content
`implement.md` must include:
- exact file paths
- ordered tasks
- interfaces, types, functions, or schema changes
- test cases or test code
- verification commands and expected results
- rollback or risk-control notes when relevant
## Placeholder ban
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
## Self-review
Before handing back to Trellis:
1. Check every acceptance criterion maps to a concrete implementation task.
2. Check every design decision maps to a file or interface.
3. Check tests cover success path, failure path, and critical edge cases.
4. Check verification commands are runnable in this repo.
5. Check no placeholder text remains.
6. Check the task is still scoped to a single implementable unit.
## Handoff
End by stating:
- which Trellis task files were created or updated
- the selected approach
- remaining assumptions
- whether the task is ready for `trellis-continue`
