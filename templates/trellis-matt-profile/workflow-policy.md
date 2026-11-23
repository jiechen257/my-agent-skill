# Local Workflow Policy

This local policy takes precedence over older dispatch and auto-commit instructions in this workflow.

1. Default to working directly without a new Trellis task. Create a task or child task only when the user explicitly requests its creation. Complexity, cross-session work, an existing `.trellis/`, or selecting a skill does not authorize creation. Do not routinely ask whether to create a task.
2. Resume a clearly matching existing task. If none matches and creation was not explicitly requested, continue directly with the matching Matt method. For existing or explicitly requested tasks, use the project's planning and review gates before `task.py start`.
3. The main session owns exploration, implementation, review, and acceptance. Sub-agents run only when the user explicitly requests them or explicitly selects a workflow that requires them.
4. Keep `codex.dispatch_mode: inline` and `session_auto_commit: false`. Retained agent definitions are optional compatibility assets.
5. Context order is `prd.md` → optional `design.md` / `implement.md` → spec and research files referenced by the task's jsonl manifest. Read the manifest files directly in the main session.
6. Missing optional artifacts do not justify creating boilerplate. Preserve task, spec, workspace, journal, and runtime records.
7. Promote stable verified knowledge to specs only after user confirmation. Finish/archive and journal recording never imply commit, push, or PR authorization.
8. When no task is active, the per-turn hook is silent. It never bootstraps Trellis or requests task-creation consent. Global and project rules handle explicit creation requests; active tasks and stale pointers still emit state.

[workflow-state:planning-inline]
Stay in planning for the current task. Read its prd.md and relevant planning artifacts, apply trellis-brainstorm/Matt methods, and use grill-me for the final adversarial review. Resolve blocking findings and obtain user confirmation before task.py start. Work in the main session.
[/workflow-state:planning-inline]

[workflow-state:in_progress-inline]
Read the active task's prd.md, optional design.md/implement.md, and context manifests. Implement, review, and verify in the main session with matching Matt methods. Keep the agreed scope and report actual evidence. Commit, push, PR, and spec promotion require explicit authorization.
[/workflow-state:in_progress-inline]

[workflow-state:completed-inline]
Confirm actual acceptance evidence, then use the project's finish workflow to archive and record the session. Do not commit, push, or create a PR without explicit user authorization.
[/workflow-state:completed-inline]
