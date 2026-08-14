---
name: code-cr-handoff
description: Use when the user asks to open a new Alibaba Code CR/PR from a local Git branch, especially when a refs/for push would update an existing review or the user wants to complete the web form themselves.
---

# Code CR Handoff

Push a real source branch, open the Code review form with the source and target selected, then hand the untouched form to the user.

## Ownership Boundary

The user owns the form and final submission.

- Do not fill the title, description, reviewers, work items, AI-review options, or any other field.
- Do not remove or accept automatically suggested reviewers.
- Do not click `提交` or otherwise create the CR.
- Do not treat the user's request to “发起 CR/PR” as permission to fill or submit the form.
- Cross this boundary only when the user explicitly overrides it in the current request.

## Workflow

### 1. Establish the branch boundary

Inspect:

```bash
git status --short --branch
git branch --show-current
git rev-parse HEAD
git remote -v
git fetch --prune origin <target-branch>
```

Preserve existing work. If uncommitted changes make the requested source ambiguous, ask whether they belong in the branch; do not commit them silently.

When the user requests a new branch, use their exact name or a unique `codex/` name. Create it from the current local `HEAD`:

```bash
git switch -c <source-branch>
```

Do not amend, cherry-pick, or add an empty commit merely to obtain a new commit ID. A branch-based Code CR does not need a rewritten patch.

Completion criterion: the source branch, source commit, target branch, target commit, and worktree state are all explicit.

### 2. Push a real source branch

```bash
git push -u origin <source-branch>
git rev-parse HEAD origin/<source-branch>
```

The two SHAs must match before continuing.

For an independent CR, do not push `HEAD:refs/for/<target-branch>`. Alibaba Code can reuse the current user's open review for that target and update the old CR instead of creating a new one. Standard GitLab `merge_request.create` push options may also be ignored by this Code instance.

Completion criterion: the named source branch exists on `origin` and points to local `HEAD`.

### 3. Build the Code creation URL

Convert an SSH remote such as:

```text
git@gitlab.alibaba-inc.com:<group>/<repo>.git
```

to this URL, URL-encoding both branch values:

```text
https://code.alibaba-inc.com/<group>/<repo>/codereview/new?from=<target-branch>&to=<source-branch>
```

In Code, `from` is the target branch and `to` is the source branch. Do not trust a server-generated link that defaults `from=master`; replace it with the user's exact target.

### 4. Hand off the untouched form

Open the creation URL in an authenticated browser when available. Prefer a new tab so an existing CR page is not repurposed.

Verify only:

- 来源分支 equals `<source-branch>`
- 目标分支 equals `<target-branch>`
- the displayed source commit matches local `HEAD`
- the changed-file count is plausible

Stop there. Leave the creation page open for the user to fill and submit. If browser access is unavailable, return the creation URL instead.

Completion criterion: the remote branch is ready and the correctly targeted, untouched creation form is open or linked. A CR does not exist yet.

## Failure Handling

- If a `refs/for` push updated an old CR, report the old CR number and do not hide the mutation.
- Do not abandon, close, or modify the old CR unless the user explicitly requests it.
- If Code shows the wrong branches, correct the URL parameters rather than editing form fields.
- If the target moved after the push, report the drift and ask whether to rebase; do not rewrite history automatically.

## Handoff Report

Report the source branch, source SHA, target branch, creation URL, and worktree state. State explicitly that the form was not filled or submitted and that the user must finish it.

Do not emit a successful PR-created signal or claim the CR was created before the user submits the form.
