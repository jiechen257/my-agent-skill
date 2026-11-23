---
name: trellis-start
description: "Initialize or resume a Trellis-managed session, load project context, and route work through the local Trellis + Matt profile. Use when beginning a coding session, starting a durable task, or re-establishing project context."
---

# Start Session

Initialize a Trellis-managed development session. This platform has no session-start hook, so manually load the equivalent context by following these steps (each one mirrors a section the hook would otherwise inject).

## Task creation boundary

Do not create a Trellis task or child task unless the user explicitly requests its creation. Task complexity, cross-session work, an existing `.trellis/` directory, or selecting a Trellis skill does not grant that authorization. Reuse a clearly matching existing task; otherwise work directly with the matching Matt method without creating Trellis artifacts or routinely asking whether to create a task. If `.trellis/` is absent, do not initialize it unless the user explicitly requests initialization.

---

## Step 1: Current state
Identity, git status, current task, active tasks, journal location.

```bash
python3 ./.trellis/scripts/get_context.py
```

## Step 2: Workflow overview
Phase Index + skill routing table + DO-NOT-skip rules.

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
```

Full guide in `.trellis/workflow.md` (read on demand).

## Step 3: Guideline indexes
Discover packages + spec layers, then read each relevant index file.

```bash
python3 ./.trellis/scripts/get_context.py --mode packages
cat .trellis/spec/guides/index.md
cat .trellis/spec/<package>/<layer>/index.md   # for each relevant layer
```

Index files list the specific guideline docs to read when you actually start coding.

## Step 4: Decide next action
From Step 1, route by task status and artifact state:

- **No durable task needed** → work Inline; do not create Trellis artifacts.
- **No active task** → inspect unfinished tasks with `python3 ./.trellis/scripts/task.py list --mine`. Resume a clear match: for `planning`, keep its path explicit and do not run `task.py start` until the review gate passes; for `in_progress`, run `task.py start <task-path>` to restore the session pointer. If several tasks could match, ask which one to resume. If none matches, create a task through `trellis-brainstorm` only when the user explicitly requested creation; otherwise work directly without a task.
- **`status=planning`** → finish `trellis-brainstorm`, then load `grill-me`. Resolve blocking findings, curate sub-agent context, obtain user confirmation, and run `task.py start`.
- **`status=in_progress` + implementation pending** → when the project has `.codex/agents/trellis-matt-implement.toml` and `codex.dispatch_mode: sub-agent`, dispatch it with an `Active task: <path>` first line; otherwise run the matching Matt method in the main session.
- **Implementation complete** → when `.codex/agents/trellis-matt-check.toml` is available, dispatch it after implement finishes; otherwise run the matching review method in the main session.
- **Check complete** → main session verifies acceptance, considers optional spec promotion, then uses `trellis-finish-work`.

---

## Skill routing (quick reference)

| User intent | Skill |
|---|---|
| Existing task needs planning, or user explicitly requests a new Trellis task | `trellis-brainstorm` |
| Planning artifacts ready for pressure review | `grill-me` |
| Implement an active task on configured Codex projects | `trellis-matt-implement` sub-agent |
| Review an implementation on configured Codex projects | `trellis-matt-check` sub-agent |
| Stuck / repeated failed fixes | Matt `diagnosing-bugs` or `trellis-break-loop` |
| Stable reusable knowledge candidate | `trellis-update-spec` after user confirmation |

Full rules + anti-rationalization table in `.trellis/workflow.md`.
