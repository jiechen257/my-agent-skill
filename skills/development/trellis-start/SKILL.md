---
name: trellis-start
description: "Initialize or resume a Trellis-managed session, load project context, and route work through the local Trellis + Matt profile. Use when beginning a coding session, starting a durable task, or re-establishing project context."
---

# Start Session

Initialize a Trellis-managed development session. This platform has no session-start hook, so manually load the equivalent context by following these steps (each one mirrors a section the hook would otherwise inject).

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
- **No active task + durable work** → first run `python3 ./.trellis/scripts/task.py list --mine` and inspect unfinished tasks. If one clearly matches the request, resume that task instead of creating a duplicate: for `planning`, keep its path explicit while editing artifacts and do not run `task.py start` until the review gate passes; for `in_progress`, run `task.py start <task-path>` to restore the current session pointer. If several tasks could match, ask the user which one to resume. Only when none matches should you load `trellis-brainstorm` and create a task.
- **`status=planning`** → finish `trellis-brainstorm`, then load `grill-me`. Resolve blocking findings, curate sub-agent context, obtain user confirmation, and run `task.py start`.
- **`status=in_progress` + implementation pending** → when the project has `.codex/agents/trellis-matt-implement.toml` and `codex.dispatch_mode: sub-agent`, dispatch it with an `Active task: <path>` first line; otherwise run the matching Matt method in the main session.
- **Implementation complete** → when `.codex/agents/trellis-matt-check.toml` is available, dispatch it after implement finishes; otherwise run the matching review method in the main session.
- **Check complete** → main session verifies acceptance, considers optional spec promotion, then uses `trellis-finish-work`.

---

## Skill routing (quick reference)

| User intent | Skill |
|---|---|
| New durable feature / unclear requirements | `trellis-brainstorm` |
| Planning artifacts ready for pressure review | `grill-me` |
| Implement an active task on configured Codex projects | `trellis-matt-implement` sub-agent |
| Review an implementation on configured Codex projects | `trellis-matt-check` sub-agent |
| Stuck / repeated failed fixes | Matt `diagnosing-bugs` or `trellis-break-loop` |
| Stable reusable knowledge candidate | `trellis-update-spec` after user confirmation |

Full rules + anti-rationalization table in `.trellis/workflow.md`.
