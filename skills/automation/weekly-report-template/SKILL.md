---
name: weekly-report-template
description: Use when the user wants a weekly report generated from git commits for one or more specified repositories, especially for 周报, 周进展, repo-scoped weekly summaries, or when the report should cover only named code repositories within a given week.
---

# weekly-report-template

Turn repository activity into a weekly report that matches the required format. Treat git history as the primary evidence source, respect the user-provided repository scope, and default the report owner to `陈洁` unless the user explicitly names someone else.

## Source Priority

Use sources in this order:

1. user-specified repository list or absolute repository paths
2. `git log` within the target date range
3. `git status --short` and `git diff --stat` for ongoing work
4. user-provided notes, only as optional supplementary context

Do not depend on `daily/` reports or `projects/` summaries by default.
Use git evidence as the content boundary. Do not invent progress, milestones, or plans that are not supported by the repository evidence.

## Required Inputs

- date range: explicit week range from the user when available
- repository scope: one or more named repositories or absolute paths

If the user names repositories such as `qianwen-card-open` or `js-sdk-admin-service`, inspect only those repositories.
If a repository name is ambiguous, ask for the path only when the path cannot be resolved safely from local context.

If the user does not specify repositories, default to the current repository only.

## Default Scope

- Default report owner: `陈洁`
- Repository scope follows explicit user input first
- If the user explicitly names another owner or a different scope, follow the user

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

If a specified repository has no commits in the target range and no meaningful working tree changes, omit it from the ordered workstreams unless the user explicitly wants zero-activity repositories listed.

## Required Format

Always organize the final weekly report by repository. Do not use section headings such as `## 本周进展概述` in the body.

Each top-level ordered item represents one repository in scope. Inside each ordered item, use unordered child lists for the four fixed fields.

Required body shape:

```markdown
1. [仓库名 / 主题名]
   - 本周进展概述：[一句话概述：什么事情做到了什么程度 / 上了什么 / 当前使用或验证状态如何]
   - 本周进展明细：
     - [子模块 / 子主题]
       - [细节 1]
       - [细节 2]
   - 下周里程碑：[一句话概述：下周最值得期待的结果]
   - 下周计划明细：
     - [具体工作项]
     - [具体工作项]

2. [第二个仓库]
   - ...
```

Read [`references/weekly-format.md`](./references/weekly-format.md) before writing when the user mentions模板、格式要求、周进展指引、语雀模板、截图格式.

## Rewrite Rules

- Rewrite git evidence into the required structure
- Group commits by workstream or module, not by chronological 流水账
- Compress process chatter into action-and-result language
- Keep the overview and milestone to one sentence each
- Expand the detail sections with modules,方案要点,问题修复,功能接入, or key decisions when they matter
- Preserve factual boundaries from the repositories in scope
- Use ordered-list top levels and unordered-list child levels consistently
- Keep `下周里程碑` and `下周计划明细` inside each repository item
- Respect the repo filter strictly; do not pull in themes from repositories outside the requested scope

Use these normalization rules:

- If many commit messages repeat the same noun or subsystem, cluster them into one workstream
- If commit messages show repeated fixes around one topic, summarize that topic as a stabilization or收边 stream
- If git evidence lacks an adoption or usage signal, write rollout, integration, or validation state instead
- If git evidence lacks a clear next-week milestone for a repository, derive one from the highest-frequency unfinished theme in that repository and phrase it as a planned target
- If git evidence lacks detailed next-week tasks for a repository, extract them conservatively from repeated change themes and current working tree signals in that repository

## Writing Guidance

Write direct Chinese prose.

For `本周进展概述`, prefer a sentence shaped like:

- `完成 X 收口，Y 已进入 Z，当前重点转到 W。`
- `推进 X 到 Y 阶段，Z 已具备可用能力，下一步聚焦 W。`

For `下周里程碑`, prefer a sentence shaped like:

- `下周目标是完成 X，并形成 Y。`
- `下周重点是打通 X，推动 Y 进入可验证状态。`

For `本周进展明细`, prefer 2 to 5 grouped bullets under each ordered item:

- one bullet per module, workstream, or theme
- include result first, then method or issue when useful
- keep each bullet self-contained and readable outside the original source context

For `下周计划明细`, list concrete tasks as child bullets:

- use action verbs
- keep items specific enough to verify later
- avoid vague lines such as `持续优化` or `继续推进`

## Output Skeleton

Use this skeleton unless the user asks for a different title or extra sections:

```markdown
# 陈洁周报

- 周期：YYYY-MM-DD 至 YYYY-MM-DD
- 范围：repo-a、repo-b
- 来源：Git 提交记录、工作区变更

1. [仓库 1]
   - 本周进展概述：[一句话概述]
   - 本周进展明细：
     - [子主题 1]
       - [细节 1]
       - [细节 2]
   - 下周里程碑：[一句话概述]
   - 下周计划明细：
     - [计划 1]
     - [计划 2]

2. [仓库 2]
   - 本周进展概述：[一句话概述]
   - 本周进展明细：
     - [子主题 1]
       - [细节 1]
   - 下周里程碑：[一句话概述]
   - 下周计划明细：
     - [计划 1]
```

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

In those cases, prefer the relevant daily-summary or commit-summary skill, or return the template directly.

## Quality Checklist

Before finishing, verify:

- [ ] The report uses ordered-list top levels and unordered-list child levels
- [ ] Every repository item contains all four fixed fields
- [ ] `本周进展概述` and `下周里程碑` are each one sentence
- [ ] `本周进展明细` is grouped by theme, not chronology
- [ ] `下周计划明细` contains concrete tasks under each repository item
- [ ] The report does not invent facts beyond the git evidence
- [ ] The report includes only repositories in the requested scope
- [ ] The report defaults to `陈洁` unless the user requested another owner
