---
name: trellis-finish-work
description: "Finish a Trellis task without automatic git operations: verify acceptance evidence, consider optional spec promotion, archive the task, and record the session. Use when implementation and review are complete."
---

# Finish Work

Close the Trellis lifecycle. Do not commit, push, or open a PR.

## 1. Survey state

```bash
python3 ./.trellis/scripts/get_context.py --mode record
git status --short
```

Identify the active task, its acceptance criteria, completed validation, current dirty paths, and any unrelated user work. Do not modify or include unrelated changes.

Completion criterion: every dirty path is classified as current-task work, unrelated work, or uncertain.

## 2. Verify the finish gate

Confirm that:

- `trellis-matt-check` or an equivalent project review completed.
- Required lint, typecheck, tests, builds, or runtime checks have recorded results.
- Acceptance criteria are met, or any exception is explicitly documented.
- No unresolved finding requires more implementation or a product decision.

If the gate is not met, return to the relevant phase. A dirty working tree is allowed and is not a reason to commit automatically.

Completion criterion: the task is genuinely complete and the remaining dirty state is accurately reported.

## 3. Consider spec promotion

If review found stable, reusable, verified knowledge, load `trellis-update-spec`. It will show the proposed change and wait for user confirmation. Skip this step when the result is task-local or already documented.

Completion criterion: each spec candidate is promoted, declined, or explicitly deferred.

## 4. Archive the task

Before running any Trellis record/archive script, verify `.trellis/config.yaml` explicitly contains `session_auto_commit: false`. If it does not, stop and ask whether to set that project-local safety boundary; never run an auto-committing archive or journal command implicitly.

```bash
python3 ./.trellis/scripts/task.py archive <task-name>
```

Archive only tasks whose finish gate passed. With `session_auto_commit: false`, this updates Trellis files without staging or committing them.

Completion criterion: the selected task is archived and no git operation was performed.

## 5. Record the session

```bash
python3 ./.trellis/scripts/add_session.py \
  --title "Session Title" \
  --commit "<explicit user-requested commit hashes, or none>" \
  --summary "Brief evidence-bounded summary"
```

Record actual commit hashes only when commits already exist because the user explicitly requested them. Otherwise use `none`.

Completion criterion: the journal records the outcome, validation evidence, remaining risks, and current git state without creating a commit.

## 6. Report

Return:

- Task archived
- Validation evidence
- Spec promotion result
- Dirty files intentionally left uncommitted
- Remaining risks
