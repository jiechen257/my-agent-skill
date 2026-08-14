---
name: trellis-update-spec
description: "Promote stable, reusable, verified project knowledge into .trellis/spec after showing the proposed change and receiving user confirmation. Use after implementation, debugging, or review produces a durable contract or convention."
---

# Promote Trellis Spec

Promote durable knowledge; do not turn task history into global rules.

## 1. Apply the promotion gate

A candidate qualifies only when all are true:

- Stable: expected to remain true beyond the current task.
- Reusable: future work in the same area needs it.
- Verified: supported by code, tests, runtime evidence, or an explicit decision.
- Missing: not already captured by an existing spec.

Reject one-off implementation details, temporary workarounds, incident timelines, speculative advice, and facts already obvious from the code.

Completion criterion: every candidate is classified as promote, task-local, duplicate, or unverified.

## 2. Locate the single source of truth

Read the relevant spec index and target file. Search for the concept before creating a new section or file. Prefer updating the existing contract closest to the behavior.

For a shared contract, include the concrete signature, payload/schema fields, boundary behavior, validation/error cases, and required tests that future implementation needs. Keep higher-level guides as short pointers rather than duplicated detail.

Completion criterion: one authoritative target is selected and duplication is ruled out.

## 3. Present the proposed update

Show the user:

- Candidate knowledge
- Evidence
- Target file and section
- Exact proposed wording or diff

Wait for explicit confirmation before editing `.trellis/spec/`. If the user declines, leave the candidate in the task record.

Completion criterion: the user explicitly approves, edits, defers, or rejects the proposal.

## 4. Update and verify

After approval, make the smallest spec edit. Update an index only when discoverability changes. Run the repository's documentation or Trellis validation command when available, then inspect the final diff for accidental task-local detail.

Do not stage or commit the change.

Completion criterion: the approved knowledge exists once in the correct spec location and validation evidence is recorded.
