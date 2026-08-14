# Workflow Policy Overlay

Apply these rules to the target project's local `.trellis/workflow.md`:

1. Simple, local work remains Inline. Durable work uses Trellis task state and planning artifacts.
2. Planning is owned by `trellis-brainstorm`; `grill-me` is the adversarial review gate before `task.py start`.
3. Before creating a task, inspect unfinished tasks and resume a clear match instead of duplicating it.
4. Codex runs implementation and check in the main session using the matching Matt methods; it does not proactively dispatch sub-agents.
5. Keep `codex.dispatch_mode: inline`. Retained `trellis-matt-*` agent definitions are rollback assets and run only after an explicit user request.
6. Context order is `prd.md` → optional `design.md` / `implement.md` → spec and research files referenced by the jsonl manifest.
7. The main session owns implementation, check, and final acceptance. Spec promotion is optional and requires user confirmation.
8. `trellis-finish-work` may archive a dirty tree but never commits automatically.
9. Commit, push, and PR operations run only after an explicit user request.

The installed workflow is project-local runtime configuration. Do not add it to the target project's version control.
