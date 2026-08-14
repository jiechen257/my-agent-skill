---
name: trellis-continue
description: "Resume the active Trellis task and route its next step through the local Trellis + Matt profile. Use when returning to planning, implementation, review, or finish work."
---

# Continue Current Task

Resume work on the current task — pick up at the right phase/step in `.trellis/workflow.md`.

---

## Step 1: Load Current Context

```bash
python3 ./.trellis/scripts/get_context.py
```

Confirms: current task, git state, recent commits.

If no active task is reported, run `python3 ./.trellis/scripts/task.py list --mine` before creating anything. Resume a clearly matching unfinished task instead of duplicating it. Keep a `planning` task path explicit until the grill and user-confirmation gate allows `task.py start`; for an `in_progress` task, `task.py start <task-path>` restores this session's pointer without changing its phase. Ask one question if several tasks plausibly match.

## Step 2: Load the Phase Index

```bash
python3 ./.trellis/scripts/get_context.py --mode phase
```

Shows the Phase Index (Plan / Execute / Finish) with routing + skill mapping.

## Step 3: Decide Where You Are

`get_context.py` shows the active task's `status` field. Route by `status` + artifact presence:

- `status=planning` + incomplete planning artifacts → load `trellis-brainstorm`
- `status=planning` + artifacts ready but not pressure-reviewed → load `grill-me`
- `status=planning` + grill findings resolved + manifests curated → obtain user confirmation, then run `task.py start`
- `status=in_progress` + implementation not started → dispatch `trellis-matt-implement` only when its project agent file exists and dispatch mode is `sub-agent`; otherwise use the main-session Matt method
- `status=in_progress` + implementation done, not yet checked → dispatch `trellis-matt-check` only when available, after implement finishes; otherwise review in the main session
- `status=in_progress` + check passed → main session verifies acceptance, considers optional spec promotion, then finishes
- archived/completed task → there is normally no active pointer; inspect the archive only when the user explicitly wants historical context

Phase rules (full detail in `.trellis/workflow.md`):

1. Keep `trellis-brainstorm` as planning owner and `grill-me` as its review gate.
2. Keep one writing agent active: implement first, check second.
3. Trellis child agents do not spawn descendants; the main session may still use ordinary Codex sub-agents.
4. Never commit, push, or open a PR unless the user explicitly asks.

## Step 4: Load the Specific Step

Once you know which step to resume at:

```bash
python3 ./.trellis/scripts/get_context.py --mode phase --step <X.X> --platform codex
```

Follow the loaded instructions. After each `[required]` step completes, move to the next.

---

## Reference

Full workflow, skill routing table, and the DO-NOT-skip table live in `.trellis/workflow.md`. This command is only an entry point — the canonical guidance is there.
