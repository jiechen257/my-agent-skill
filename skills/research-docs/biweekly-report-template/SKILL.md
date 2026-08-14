---
name: biweekly-report-template
description: Merge two weekly reports into an evidence-bounded biweekly report. Use for 双周报、最近两周 or biweekly requests, including personal four-section reports and explicitly requested portfolio or module variants.
---

# Biweekly Report Template

Consolidate weekly source material without upgrading its claims. Follow these five steps in order.

## 1. Resolve the period, sources, and mode

Use the period and inputs named by the user. Otherwise select the latest two weekly reports that plausibly cover the requested owner and business scope; do not silently replace them with Git history.

Choose one mode:

- `personal` by default: one unified four-section narrative.
- `portfolio` only when the user asks for a multi-project review, project portfolio,推进索引, or priority view.
- `module` only when the user asks for embeddable module material or a module-format report.

Read the actual `周期`, `来源`, and `统计口径` from both source reports.

**Complete when:** the intended owner, source files, inclusive period candidate, and one output mode are explicit.

## 2. Prove period continuity

Compute the union of source date ranges before merging. Two default weekly sources must form one gap-free, overlap-free 14-day closed interval.

If sources overlap or leave a gap, stop the merge and ask one question that names the conflicting dates. Do not silently double-count or bridge missing days. A user-explicit non-14-day period may continue, but preserve its actual dates in the metadata and pass the validator override.

Use the validator early when useful. Resolve `SKILL_DIR` to the absolute directory containing this `SKILL.md`; never resolve the validator relative to the current working directory:

```bash
SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/validate_biweekly.py" <draft-or-fixture> \
  --source <week-1> --source <week-2>
```

**Complete when:** every day in the report period has exactly one source interval, or the user explicitly accepted a named non-standard period.

## 3. Consolidate the evidence ledger

Treat the two weekly reports as the primary evidence. Preserve their completion and release boundaries. Git may only fill a documented gap, resolve a conflict, or satisfy an explicit request to recollect evidence; when used, apply the weekly skill's owner filtering and evidence rules.

Do not promote `开发中` to `待提测`, `待提测` to `已提测`, or any status to `已上线` / `已完成` without an input that states the promoted status. Keep working-tree signals as ongoing work only.

**Complete when:** every merged claim maps to a source report, conflicting claims are resolved explicitly, and no status is stronger than its strongest source.

## 4. Merge themes and render the selected branch

Merge duplicate workstreams across the two weeks and preserve meaningful transitions such as “完成基础实现，进入联调”. Read [`references/biweekly-format.md`](./references/biweekly-format.md) in full before every render; it is the single source of truth for all three modes, metadata, list markers, headings, and file naming.

Include an OKR appendix only when the user explicitly asks for OKR alignment. Read the named OKR document, add its path to `来源`, and pass `--allow-okr` during validation.

**Complete when:** themes are deduplicated, the selected mode is followed exactly, status wording is source-backed, and optional OKR content has both explicit authorization and a cited source.

## 5. Validate and save

Run the self-contained validator with the actual source reports:

```bash
SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/validate_biweekly.py" <report-file> \
  --mode personal \
  --source <week-1> --source <week-2>
```

Use `--mode portfolio` or `--mode module` for those explicit branches. Add `--allow-nonstandard-period` only after the user explicitly selects that date range, and `--allow-okr` only after an explicit OKR request.

Fix every reported error before claiming completion. When saving, follow the target repository's `AGENTS.md`, then the format reference.

**Complete when:** the validator exits zero, the report is saved or returned in the requested mode, and its sources, dates, statuses, and headings match the selected branch.
