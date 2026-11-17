---
name: weekly-report-template
description: Generate evidence-based weekly reports for 周报、上周进展、周进展 and repo-scoped weekly summaries. Defaults to 之瓷's OKR-based weekly report. Use a biweekly workflow for 双周报、最近两周 or biweekly requests.
---

# Weekly Report Template

## 1. Select the report format and scope

- For 之瓷's weekly report, including an unqualified “生成上周周报” from this user, use the [personal weekly format](references/personal-weekly-format.md) by default. Use the three metrics in [personal weekly metrics](references/personal-weekly-metrics.md). The progress groups are 录音纪要、Query 抽检平台、其他. The plan has separate 本周 and 下周 columns.
- For a different owner or an explicitly requested general report, use [the general format](references/weekly-format.md). Read [general metric analysis](references/weekly-metric-analysis.md) when that report includes metrics. Respect a user-specified format or scope for the individual report.
- Use an explicit date range when supplied. Otherwise resolve 上周 as the most recent completed Tuesday–Monday interval in Asia/Shanghai. For comparisons use the immediately preceding equal-length interval with the same filters. Use inclusive dates in the report and half-open query intervals in iTrace. Date the personal report's plan columns by the Monday of each team planning week as shown in the format reference.
- Use the business repositories the user names. Otherwise start with the latest relevant report and established scope, then inspect recent owner activity to identify candidate repositories. Ask a focused scope question only if a material ambiguity remains. Never select the `daily-report` repository as the default business scope. Its reports and OKRs can serve as sources.

## 2. Collect the owner's evidence

Use the requested owner or confirm the current user's Git identity against the relevant repository history. Do not treat commits from other authors as the owner's work. Inspect ordinary business refs as needed to recover merged or rebased work. Treat stash and refs named `backup`, `archive`, or `before-squash` as attribution clues unless the commits also exist on an ordinary business ref.

Filter by verified author and deduplicate by commit hash across branches and worktrees:

```bash
git -C <repo> log --all --no-merges --author='<escaped owner email or name>' \
  --since='YYYY-MM-DD 00:00:00 +0800' --until='YYYY-MM-DD 23:59:59 +0800' \
  --pretty=format:'%H%x09%aI%x09%an%x09%ae%x09%D%x09%s'
```

Check the author timestamps in Asia/Shanghai after collection. Include relevant user-provided or approved task, telemetry, review and acceptance records. Git can establish what changed. Release, adoption and effect claims need their own evidence. A worktree diff can support a corroborated in-progress item or future plan.

## 3. Write the report

For 之瓷, read the current formal OKR before taking metrics. Use its goals, baselines and definitions as written, with their periods and confirmation status. In the main table cover only **Agent 任务交付成功率、Query 分析问题回收情况、无效工具调用比例**. See the personal metric reference for how to query and report each. Keep all three rows when results are missing.

A metric movement, log-query result, or problem discovery is not a delivered work item by itself. In 周进展, describe the concrete activity in the report period, its status and any evidence of acceptance. Use 其他 for verified activity outside the two main workstreams. Keep the three groups, but let the number of points follow the evidence. Do not repeat last week's examples as this week's work.

Use current user commitments or task documents for 本周 and 下周. If those are incomplete, use prior commitments, unresolved items or corroborated worktree evidence and label inferred plans. Every item must contain an object, an action, and a verifiable result. Write explicit gaps if the plan for either week is unknown. A plan to publish or review does not authorize the external action.

## 4. Render and validate

Read the selected format reference before rendering. For a saved report follow the target repository's `AGENTS.md` and use the format reference's filename rules. Use the actual absolute skill directory for the validator:

```bash
SKILL_DIR="<absolute directory containing this SKILL.md>"
python3 "$SKILL_DIR/scripts/validate_weekly.py" <report-file>
```

The default validator checks 之瓷's six sections, three metric rows, three progress groups and two plan weeks. For the general format use `--format general`. When the user supplies a different structure, check it against that structure. Independently verify the metric definitions, values, sources and actual work status. Fix any reported structural errors before delivering the selected format.
