---
name: qwork-nano-runbook
description: Use when working on QWork/Nano card development or validation, especially Nano 卡片开发大师 Step 1-4, qwen-chat-nano workspaces, qianwen-card-open MCP calls, Figma/MasterGo design input, nanocompose preview/build, stale task recovery, or agent-sdk skill injection issues.
---

# QWork Nano Runbook

Drive QWork/Nano card tasks from evidence. Treat the live QWork chain, generated artifacts, branch/workspace state, and preview reports as the acceptance surface.

## Scope

Use this skill for:

- `Nano 卡片开发大师` Step 1-4 validation
- QWork task recovery, restart decisions, and stale state diagnosis
- `qwen-chat-nano` / Nano template repo checks
- Figma or MasterGo design-input validation before generation
- `nanocompose` build/preview/report troubleshooting
- Qianwen Agent SDK local runs when skill injection or MCP auth is involved

Do not accept placeholder cards as valid output when the target design cannot be confirmed.

## Workflow

```text
[1] Establish task truth
      -> identify QWork task, card repo root, current branch, expected branch, template name, and task.localPath

[2] Preflight workspace
      -> verify repo root, .agents/skills availability, .agents/.git state, env/token caveats, and design input

[3] Gate each step by artifacts
      -> Step 1 requirement, Step 2 generated template/build marker, Step 3 preview reports, Step 4 publish/UI evidence

[4] Diagnose failures by layer
      -> UI state, repo/branch, skill root, MCP auth, Figma/design, Gradle/NanoCompose, SDK runtime

[5] Decide continue versus restart
      -> restart clean when task state, form input, output artifacts, or child processes are corrupted

[6] Report acceptance state
      -> exact completed steps, missing evidence, blocker class, and next command/UI action
```

## Preflight Checks

- Confirm the active card repo root, often under `/Users/zhici/qknow-git/cards/qwen-chat-nano`.
- Compare current branch with the expected QWork branch.
- Inspect `.agents/skills` as the source skill root; treat runtime `.skills` as a mounted layer.
- Inspect `.agents/.git` when branch operations fail with submodule or git-dir errors.
- Verify design target identity, dimensions, and language before accepting generated output.
- Keep missing Figma/Qianwen tokens as auth-context caveats unless the error directly proves auth is the root cause.

## Step Gates

- **Step 1 / `recordRequirement`**: requirement artifact exists and reflects the requested card, design source, card type, and Chinese/English expectations.
- **Step 2 / `developTemplate`**: generated `Template.kt`, `mock.json`, design spec, and build marker are present; build success alone is not enough.
- **Step 3 / `previewVerify`**: `nanocompose preview` state plus `ui-verify-report.md`, `action-verify-report.md`, and `screenshot.png` when the chain expects them.
- **Step 4 / publish/release**: QWork UI state, publish artifact, or release marker confirms terminal state.

## Failure Classes

- Stale QWork task: old child processes, corrupted form fields, half-written output, or step state that no longer matches artifacts.
- Repo-state drift: wrong `task.localPath`, wrong branch, broken `.agents` metadata, or missing initialized workspace.
- Design fallback: placeholder English hotel card, default tags, wrong size, or unconfirmed Figma node.
- Skill/runtime drift: `.agents/skills` and runtime `.skills` disagree, or native loader cannot resolve dependencies such as `ai`.
- Build/preview drift: Gradle dependency timeout, missing `nanocompose-last-build.json`, live preview without expected report artifacts.
- SDK runtime issue: timeout abort, unhandled rejection, pairing 503, or stream completion signal mismatch.

## Rules

- Separate capture-tool failures from card-preview truth.
- Prefer fresh restart over forced recovery when UI form state or generated artifacts are polluted.
- Do not merge auth/env caveats with SDK/runtime bugs unless evidence connects them.
- Preserve exact error strings, SDK beta versions, branch names, and artifact paths in handoff notes.
- Validate with the live QWork UI plus local artifacts; local compile output alone is partial evidence.

## Verification

Minimum completion evidence:

- repo root and branch checked
- expected Step 1-4 artifact status stated
- preview/build command or UI evidence reported when relevant
- blocker classified by layer when the chain does not pass
