---
name: weekly-report-template
description: Use when the user wants a weekly report generated from git commits and approved supplementary materials for one or more specified repositories, especially for 周报, 周进展, repo-scoped weekly summaries, or when the report should cover only named code repositories within a given week.
---

# weekly-report-template

Turn repository activity and approved supplementary materials into a weekly report that matches the required format. Treat git history as the primary evidence source, respect the user-provided repository scope, and default the report owner to `陈洁` unless the user explicitly names someone else.

The report is a single integrated narrative organized by **workstream / theme**, not by repository. Multiple repositories can flow into the same workstream when they share a theme; the body must not surface raw commit hashes, file counts, line counts, or copy-pasted commit subject lines.

## Evidence Model

Use a two-layer evidence model:

1. Hard evidence: repository activity inside the requested scope
2. Supplementary context: user-approved docs, chat notes, Chronicle summaries, and hand-written notes

Hard evidence decides what can be claimed as completed engineering work. Supplementary context can refine theme names, explain decisions, add coordination status, and shape next-week plans.

## Source Priority

Use sources in this order:

1. user-specified repository list or absolute repository paths
2. `git log` within the target date range
3. `git status --short` and `git diff --stat` for ongoing work
4. user-provided docs or links, such as Yuque / DingTalk / local Markdown
5. user-provided notes, meeting notes, chat summaries, or Chronicle-derived summaries

Do not depend on `daily/` reports or `projects/` summaries by default.
Use git evidence as the completion boundary. Do not invent shipped progress, milestones, or usage outcomes that are not supported by hard evidence or explicit supplementary material.

When sources conflict, prefer hard evidence for completed work and use supplementary context to describe intent, design rationale, blockers, and next steps.

## Required Inputs

- date range: explicit week range from the user when available
- repository scope: one or more named repositories or absolute paths
- optional supplementary scope: document links, chat summaries, Chronicle summaries, local notes, or copied source text
- optional output mode: chat-only Markdown, local saved Markdown, or paste-ready Yuque / DingTalk Markdown

If the user names repositories such as `qianwen-card-open` or `js-sdk-admin-service`, inspect only those repositories.
If a repository name is ambiguous, ask for the path only when the path cannot be resolved safely from local context.

If the user does not specify repositories, default to the current repository only.
If the user provides supplementary materials without a repository scope, ask for the repository scope unless the current repository is clearly the target.

## Default Scope

- Default report owner: `陈洁`
- Repository scope follows explicit user input first
- If the user explicitly names another owner or a different scope, follow the user
- Supplementary materials are opt-in. Use only the sources the user gives or explicitly approves for the weekly report.

## Git Collection Workflow

For each repository in scope:

1. Collect non-merge commits in the target range
2. Filter by explicit commit date in the final output, not only by traversal options
3. Optionally inspect current working tree changes for unfinished work
4. Group commits into a few workstreams before writing

Recommended commands:

```bash
git -C <repo> log --no-merges --pretty=format:'%h%x09%ad%x09%s' --date=short | awk -F '\t' '$2 >= "YYYY-MM-DD" && $2 <= "YYYY-MM-DD"'
git -C <repo> status --short
git -C <repo> diff --stat
```

If a specified repository has no commits in the target range and no meaningful working tree changes, omit its themes from the workstream list unless the user explicitly wants zero-activity repositories listed.

## Supplementary Material Workflow

Use supplementary materials only after hard evidence collection:

1. Read the user-approved docs, notes, or summaries
2. Extract only weekly-report-relevant facts: project background, design decisions, coordination status, blockers, next plans
3. Map each fact to an existing workstream when possible
4. Create a new workstream only when the material describes a substantial theme that is inside the requested scope
5. Mark facts as supplementary in your internal notes, then rewrite them into the final report without exposing source plumbing

Supported supplementary sources:

- Yuque / DingTalk docs: use them for solution background, alignment status, next-week plans, and cross-team coordination
- Chat summaries or copied messages: use them for collaboration progress, feedback, and open confirmations
- Chronicle summaries: use them for recent-work signals and session context, then verify central claims through repo files, docs, or user-provided text when feasible
- Local Markdown / notes: use them for design rationale, known risks, or planning context

Do not use noisy OCR text as final factual evidence. Use it only to locate the relevant document, conversation, or local note.

## Required Format

The body uses a fixed four-section structure with **mixed list markers**:

- top level: ordered list `1.` / `2.` / `3.` / `4.` for the four fixed sections
- workstream level (under `本周进展明细` and `下周计划明细`): lettered list `a.` / `b.` / `c.` / `d.`
- detail level (under each workstream in `本周进展明细`): roman numerals `ⅰ.` / `ⅱ.` / `ⅲ.` / `ⅳ.`
- indentation: 2 spaces per level

Required body shape:

```markdown
1. 本周进展概述：[一句话概述]
2. 本周进展明细：
  a. [工作流 / 主题 1]
    ⅰ. [细节 1]
    ⅱ. [细节 2]
  b. [工作流 / 主题 2]
    ⅰ. [细节 1]
3. 下周里程碑：[一句话概述]
4. 下周计划明细：
  a. [具体工作项]
  b. [具体工作项]
```

The four sections are fixed in count and order: `本周进展概述` → `本周进展明细` → `下周里程碑` → `下周计划明细`. Do not introduce additional top-level sections, and do not split the report per repository at the top level.

Group related work across repositories into a single workstream when they share a theme (for example, `协议 Mock 调试` can include both backend and web changes). When the user signals "其他" or "杂项" content (打包修复、运维问题、零散补丁), put it in a final `其他` workstream instead of inflating it into a top-level section.

Read [`references/weekly-format.md`](./references/weekly-format.md) before writing when the user mentions模板、格式要求、周进展指引、语雀模板、截图格式.

## Rewrite Rules

- Rewrite git evidence into the required structure, grouped by workstream / theme
- Compress process chatter into action-and-result language
- Keep `本周进展概述` and `下周里程碑` to one sentence each
- Expand `本周进展明细` with 模块进展、方案要点、问题修复、能力接入、关键决策, organized by workstream
- Preserve factual boundaries from the repositories in scope
- Use the mixed list markers (`1.` / `a.` / `ⅰ.`) consistently
- Respect the repo filter strictly; do not pull in themes from repositories outside the requested scope
- Merge supplementary context into the matching workstream instead of creating separate "文档" or "沟通" top-level sections
- When a claim comes only from supplementary material, phrase it as alignment, design, planning, or coordination status unless the source explicitly proves completion

Use these normalization rules:

- If many commit messages repeat the same noun or subsystem, cluster them into one workstream
- If commit messages show repeated fixes around one topic, summarize that topic as a stabilization or 收边 stream
- If git evidence lacks an adoption or usage signal, write rollout, integration, or validation state instead
- If git evidence lacks a clear next-week milestone, derive one from the highest-frequency unfinished theme and phrase it as a planned target
- If git evidence lacks detailed next-week tasks, extract them conservatively from repeated change themes and current working tree signals
- If supplementary materials contain richer module names than commit messages, use the module names from the supplementary material after confirming they fit the repo evidence
- If supplementary materials describe cross-team communication, include it only when it changes the workstream status, risk, or next step

### Anti-Patterns to Avoid

Do not surface raw repository plumbing in the report body:

- no commit hashes (`d8d6ccf`), commit subject quotes (`feat(mock): 支持...`), or shortlog excerpts
- no file counts, line counts, or `+1240 / -218` style diff stats
- no file path drops without context (`apps/server/app/lib/agent/agent-gateway.ts`); when a path matters, weave it into a sentence about what was added or changed
- no chronological 流水账 (do not list "周一 → 周二 → 周三")
- no per-commit bullets (each commit becomes a bullet); cluster commits by theme
- no separate "资料整理" workstream when the notes only support an engineering theme
- no claims like "已上线", "已推广", "效果良好" unless the source explicitly supports that status

When you need to reference a path or module, describe it in prose: `新增构建监控模块，承担打包过程的 iTrace 上报`, not `新增 buildItraceMonitor.ts（193 行）`.

## Writing Guidance

Write direct Chinese prose.

For `本周进展概述`, prefer a sentence shaped like:

- `完成 X 收口，Y 已进入 Z，当前重点转到 W。`
- `推进 X 到 Y 阶段，Z 已具备可用能力，下一步聚焦 W。`

For `下周里程碑`, prefer a sentence shaped like:

- `下周目标是完成 X，并形成 Y。`
- `下周重点是打通 X，推动 Y 进入可验证状态。`

For `本周进展明细`, prefer 3 to 5 workstreams under section `2.`:

- one workstream per module, theme, or major effort; merge cross-repo work that shares a theme
- under each workstream, 2 to 5 roman-numeral details
- include result first, then method or issue when useful
- keep each detail self-contained and readable outside the original source context

For `下周计划明细`, list concrete tasks as lettered items under section `4.`:

- use action verbs
- keep items specific enough to verify later
- avoid vague lines such as `持续优化` or `继续推进`

## Output Skeleton

Use this skeleton unless the user asks for a different title or extra sections:

```markdown
# 陈洁周报

- 周期：YYYY-MM-DD 至 YYYY-MM-DD
- 范围：[本周覆盖的工作流 / 模块主题]
- 统计口径：本周本人 Git 提交、相关调研 / 设计文档、本地工作区变更检查
- 来源：Git 提交记录、[关键文档路径或模块]
- 使用技能：`weekly-report-template`

1. 本周进展概述：[一句话概述]
2. 本周进展明细：
  a. [工作流 1]
    ⅰ. [细节 1]
    ⅱ. [细节 2]
  b. [工作流 2]
    ⅰ. [细节 1]
  c. [工作流 3]
    ⅰ. [细节 1]
  d. 其他
    ⅰ. [杂项 / 打包 / 运维 / 收边]
3. 下周里程碑：[一句话概述]
4. 下周计划明细：
  a. [计划 1]
  b. [计划 2]
  c. [计划 3]
```

Header guidelines:

- `范围` describes the workstream / theme coverage of this week, not a raw repo list
- `统计口径` documents what evidence drove the report
- `来源` lists the concrete inputs (git log + key doc paths / module directories / approved summaries)
- `使用技能` is fixed as `` `weekly-report-template` ``

## Output Modes

Choose the output mode from the user's request:

- Chat-only Markdown: return the finished report directly in the conversation
- Local saved Markdown: write the report to the resolved weekly-report directory, then report the saved path
- Paste-ready Yuque / DingTalk Markdown: return plain Markdown optimized for pasting, with no extra commentary around the report body

If the user asks for both local save and paste-ready output, save the Markdown file first and then return the same content in chat.

## Save Behavior

When the user wants the weekly report saved:

1. If the current project's `AGENTS.md` defines a weekly-report output directory, follow it
2. Else if the current repository contains `weekly/`, save into `weekly/`
3. Else ask the user where to save it, or return it in chat if no save path is requested

Default file name:

```text
YYYY-MM-DD-to-YYYY-MM-DD-weekly-summary.md
```

If the target directory already contains a different weekly report with the same default name, append a scope suffix instead of overwriting it, for example:

```text
YYYY-MM-DD-to-YYYY-MM-DD-repo-weekly-summary.md
```

## When Not to Use

Do not use this skill when:

- the user wants a same-day report grouped by project instead of a weekly report
- the user wants raw commit aggregation instead of a template-constrained weekly rewrite
- the user only wants the template itself and does not want content rewritten
- the user wants a research note, architecture explanation, or decision memo instead of a weekly progress report

In those cases, prefer the relevant daily-summary or commit-summary skill, or return the template directly.

## Quality Checklist

Before finishing, verify:

- [ ] The body uses the four fixed top-level sections (`1.` 概述 / `2.` 明细 / `3.` 里程碑 / `4.` 计划) in order
- [ ] Workstreams under `2.` use lettered markers `a.` / `b.` / `c.`; details use roman numerals `ⅰ.` / `ⅱ.` / `ⅲ.`
- [ ] Cross-repo work that shares a theme is merged into one workstream, not split by repo
- [ ] `本周进展概述` and `下周里程碑` are each one sentence
- [ ] `本周进展明细` is grouped by theme, not chronology, and contains no commit hashes / file counts / raw commit subject quotes
- [ ] `下周计划明细` lists concrete, verifiable tasks under section `4.`
- [ ] The header includes `周期 / 范围 / 统计口径 / 来源 / 使用技能` lines
- [ ] The report does not invent facts beyond hard evidence and approved supplementary materials
- [ ] The report includes only repositories in the requested scope
- [ ] The report defaults to `陈洁` unless the user requested another owner
- [ ] Supplementary context is merged into workstreams and does not appear as raw chat/doc/OCR dumps
