---
name: weekly-report-template
description: Generate a theme-based weekly report from the named owner's Git evidence and approved supplementary materials. Use for 周报、上周进展、周进展 or repo-scoped weekly summaries; do not use for 双周报、最近两周 or biweekly requests.
---

# Weekly Report Template

Produce one evidence-bounded weekly narrative. Follow these five steps in order.

## 1. Resolve the period and repository scope

Use an explicit date range when supplied. Otherwise resolve “上周” as the most recent completed Monday-through-Sunday interval in the user's timezone.

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

Use user-provided DingTalk, Yuque, local Markdown, chat summaries, or Chronicle context only when approved. Use supplementary material for design, alignment, risks, and plans; do not upgrade engineering or release status without explicit evidence.

**Complete when:** every prospective report claim has a source and evidence strength, and unsupported completion, adoption, release, or outcome claims have been removed.

## 4. Rewrite by theme

Merge related work across repositories into workstreams instead of listing repositories or commits. Allow one or more evidence-backed workstreams; never invent “其他” or extra themes to reach a target count.

Choose next-week plans in this order:

1. user-stated plans or task documents;
2. previous commitments and unresolved items;
3. corroborated working-tree signals.

If a plan is still inferred, use conservative verbs such as “验证”“收口”“推进”, not a promised outcome.

**Complete when:** every detail belongs to a coherent theme, every plan has a traceable basis, and raw hashes, commit subjects, file counts, diff statistics, and chronology have disappeared from the prose.

## 5. Render and validate

Before every render, read [`references/weekly-format.md`](./references/weekly-format.md) in full. It is the single source of truth for headings, metadata, list markers, output modes, file naming, and the final skeleton; do not reconstruct the format from this file.

When saving, follow the repository's `AGENTS.md`, then the format reference. Resolve `SKILL_DIR` to the absolute directory containing this `SKILL.md`; never resolve the validator relative to the current working directory. Run:

```bash
SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/validate_weekly.py" <report-file>
```

Fix every reported error before claiming completion.

**Complete when:** the validator exits zero, the saved path matches the requested output mode, and the report contains only evidence-backed repositories and claims.
