---
name: weekly-report-template
description: Generate a theme-based weekly report from the named owner's Git evidence and approved supplementary materials. Use for 周报、上周进展、周进展 or repo-scoped weekly summaries; do not use for 双周报、最近两周 or biweekly requests.
---

# Weekly Report Template

Produce one evidence-bounded weekly narrative. Follow these five steps in order. The default saved report is a strict five-section document: `阶段目标`、`数据看板 & 分析`、`周进展`、`遗留问题`、`本周目标与计划`.

## 1. Resolve the period and repository scope

Use an explicit date range when supplied. Otherwise resolve “上周” as the most recent completed Monday-through-Sunday interval in the user's timezone. The report uses an inclusive closed date range; if a data service uses half-open timestamps, its end is the following Monday at 00:00.

Resolve business repositories in this order:

1. Use repositories or absolute paths named by the user.
2. Read `来源` and `统计口径` from the latest relevant weekly reports, then inspect recent owner activity under `~/work-pro` to form candidates.
3. If more than one plausible candidate remains, ask one scope question and wait for the answer.

Never select the `daily-report` repository as the default business scope. Include it only when the user explicitly requests report-repository maintenance.

**Complete when:** the inclusive date range and every business repository path are explicit, and no unresolved scope candidate remains.

## 2. Resolve the owner and usable refs

Use the owner named by the user. Otherwise default the report owner to `陈洁`, and resolve that person's Git author names and emails from repository history and local Git configuration. Do not treat commits from other authors as the owner's work.

Inspect ordinary business refs needed to recover rebased or merged work. Treat refs whose names contain `backup`, `archive`, or `before-squash` as attribution clues only; commits found only on those refs cannot prove completion.

Collect with an author filter and full hashes, then deduplicate by commit hash. A suitable starting point is:

```bash
git -C <repo> log --all --no-merges --author='<escaped owner email or name>' \
  --since='YYYY-MM-DD 00:00:00' --until='YYYY-MM-DD 23:59:59' \
  --pretty=format:'%H%x09%aI%x09%an%x09%ae%x09%D%x09%s'
```

Verify commit dates explicitly after collection instead of relying only on traversal flags.

**Complete when:** owner aliases are explicit, every retained commit belongs to the owner and target period, hashes are unique, and backup-only evidence is marked non-completing.

## 3. Build the evidence ledger

For each repository, record completed work from retained commits and approved documents. Inspect `git status --short` and `git diff --stat` only for unfinished-work signals: working-tree changes may support “进行中” or a next-week plan, but never “已完成”, and they are not attributed to the owner without corroboration.

Classify every source-backed fact into exactly one of these buckets before writing prose:

1. **Metric or quality result**: traffic, success/failure rate, latency, error distribution, and trend. These facts belong in `数据看板 & 分析`.
2. **Delivered work item**: a feature, requirement point, bug fix, integration, investigation deliverable, or validation completed during the report period. These facts belong in `周进展` and must name what changed and its user or system effect.
3. **Current-week work item**: a concrete feature, requirement point, bug fix, integration, release, or validation action supported by a task document, user commitment, unresolved item, or corroborated worktree signal. These facts belong in `本周目标与计划`.

A metric movement, log-query result, or problem discovery is not a delivered work item by itself. It may explain the priority or effect of a delivered or planned work item, but it must not replace that work item.

Use user-provided DingTalk, Yuque, local Markdown, chat summaries, or Chronicle context only when approved. Use supplementary material for design, alignment, risks, and plans; do not upgrade engineering or release status without explicit evidence. A worktree change can support “进行中” or a plan, never “已完成”.

**Complete when:** every prospective report claim has a source and evidence strength, and unsupported completion, adoption, release, or outcome claims have been removed.

## 4. Rewrite by theme

Merge related work across repositories into workstreams instead of listing repositories or commits. Allow one or more evidence-backed workstreams; never invent “其他” or extra themes to reach a target count. Put the narrative into the five required sections:

1. `阶段目标`: state the quality or delivery target for the period.
2. `数据看板 & 分析`: state the denominator, PV/UV, success or failure rate, trend, top causes, and evidence limits when metrics are available.
3. `周进展`: lead with the concrete features, requirement points, bug fixes, integrations, or validation deliverables completed during the period, then state their effect. Do not use pure metric trends, log analysis, or failure-rate movements as progress items.
4. `遗留问题`: list unresolved defects, dependencies, and evidence gaps; write an explicit no-new-issues statement when empty.
5. `本周目标与计划`: name the concrete features, requirement points, bug fixes, integrations, release actions, or validations to execute in the current week. Every item must contain an object, an action, and a verifiable result; “保持指标稳定” or “跟进异常” alone is not a plan.

Choose next-week plans in this order:

1. user-stated plans or task documents;
2. previous commitments and unresolved items;
3. corroborated working-tree signals.

If a plan is still inferred, use conservative verbs such as “验证”“收口”“推进”, not a promised outcome.

**Complete when:** every `周进展` item maps to completion evidence, every `本周目标与计划` item maps to a plan source, metrics are not used as proxies for work items, every detail belongs to a coherent theme, and raw hashes, commit subjects, file counts, diff statistics, and chronology have disappeared from the prose.

## 5. Render and validate

Before every render, read [`references/weekly-format.md`](./references/weekly-format.md) in full. It is the single source of truth for headings, metadata, list markers, output modes, file naming, and the final skeleton; do not reconstruct the format from memory. The validator rejects the legacy four-section headings and any missing required section.

When saving, follow the repository's `AGENTS.md`, then the format reference. Resolve `SKILL_DIR` to the absolute directory containing this `SKILL.md`; never resolve the validator relative to the current working directory. Run:

```bash
SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/validate_weekly.py" <report-file>
```

Fix every reported error before claiming completion.

**Complete when:** the validator exits zero, the saved path matches the requested output mode, and the report contains only evidence-backed repositories and claims.
