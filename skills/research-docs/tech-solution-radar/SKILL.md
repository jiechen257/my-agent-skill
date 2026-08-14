---
name: tech-solution-radar
description: Use when researching community or industry best practices, open-source alternatives, libraries, frameworks, SaaS products, architecture patterns, or technical solutions that need evidence-backed comparison, popularity signals, functional fit scoring, ranking, and a recommendation.
---

# tech-solution-radar

Use this skill to turn broad technical research into a ranked decision table. It is for solution discovery, best-practice research, library/framework selection, open-source alternative comparison, vendor/tool shortlist creation, and technology radar style recommendations.

## Scope

Best fit:
- community or industry best-practice research
- technical solution comparison and ranking
- open-source/library/framework/tool/vendor shortlist
- "which option should I use" questions with feature and popularity criteria

Use `research-note-wrap` after this skill when the user wants the final research saved as a reusable Markdown note.

## Inputs

| Input | Meaning |
| --- | --- |
| `topic` | The technical problem, domain, or solution category |
| `scenario` | The user's actual usage context, product constraints, stack, scale, or team needs |
| `must_have` | Required capabilities or hard constraints |
| `nice_to_have` | Optional capabilities that affect ranking |
| `time_window` | Recency scope for popularity and maintenance signals; default to current state |
| `output_depth` | `quick`, `standard`, or `deep`; default to `standard` |

Ask at most one clarification question when the scenario or hard constraints are missing and the ranking would otherwise be misleading. If a safe assumption exists, state it and proceed.

## Workflow

```text
[1] Frame the decision
      -> define scenario, hard constraints, exclusion rules, and ranking objective

[2] Build candidate set
      -> collect 5-10 plausible options from official docs, source repos, package registries, credible community posts, and known industry references
      -> include direct substitutes first, then adjacent patterns only when useful

[3] Verify sources
      -> prefer primary sources: official docs, GitHub repos, release notes, package registries, standards, vendor docs
      -> use community content for adoption signals and practical tradeoffs
      -> browse for current facts when popularity, versions, maintenance, pricing, or product status matters

[4] Score candidates
      -> score each option on functional fit, popularity/adoption, maintenance health, ecosystem maturity, implementation cost, and risk
      -> normalize volatile metrics instead of comparing raw numbers blindly

[5] Rank and recommend
      -> produce a ranked table, explain the top recommendation, and state boundary conditions
      -> include confidence and evidence gaps
```

## Default Scoring Model

Use this default when the user does not provide weights:

| Dimension | Weight | What to check |
| --- | ---: | --- |
| Functional fit | 45% | Covers must-have capabilities, integration shape, extensibility, operational fit |
| Popularity/adoption | 25% | GitHub stars, forks, downloads, dependents, community mentions, ecosystem usage |
| Maintenance health | 20% | Recent releases, commit activity, issue/PR response, maintainer or vendor stability |
| Implementation risk | 10% | Migration cost, complexity, lock-in, security/compliance risk, learning curve |

Adjust weights explicitly when the scenario makes another dimension dominant. For internal infrastructure and long-lived systems, increase maintenance health and risk. For exploratory prototypes, increase functional fit and implementation cost. For ecosystem bets, increase adoption and integration maturity.

## Popularity Signals

Use multiple signals because each one can be gamed or biased:
- GitHub: stars, star growth when available, forks, contributors, releases, issue/PR activity
- Package registries: npm/PyPI/Maven/Go/Rust downloads, dependents, version freshness
- Ecosystem: framework integrations, plugin count, docs quality, examples, Stack Overflow/community mentions
- Industry: official adoption stories, standardization, cloud/vendor support, enterprise references

State the snapshot date for volatile signals. Avoid treating stars alone as quality.

## Output Format

Start with the recommendation, then show the evidence.

```md
## 推荐结论
推荐：<option>
理由：<1-2 sentences>
适用边界：<when this recommendation holds>

## 排名表
| Rank | 方案 | 总分 | 功能匹配 | 热门度 | 维护健康 | 风险 | 结论 |
| ---: | --- | ---: | ---: | ---: | ---: | ---: | --- |
| 1 | ... | ... | ... | ... | ... | ... | ... |

## 证据表
| 方案 | 关键能力 | 热度信号 | 维护信号 | 主要风险 | 来源 |
| --- | --- | --- | --- | --- | --- |
| ... | ... | ... | ... | ... | ... |

## 选择建议
- 直接采用：...
- 谨慎试点：...
- 暂不采用：...
```

## Rules

- Use Simplified Chinese by default.
- Lead with a clear recommendation.
- Keep direct substitutes ahead of adjacent alternatives.
- Separate facts, inference, and preference.
- Include source links for ranked claims when browsing was used.
- Treat popularity and maintenance facts as time-sensitive.
- Do not over-rank candidates when evidence is weak; use tiers when scores are too close.
- Do not recommend a solution that misses a hard constraint, regardless of popularity.

## Verification

Before finalizing:
- Check every top-ranked option against all hard constraints.
- Confirm volatile facts with current sources when they affect ranking.
- Mark assumptions and evidence gaps explicitly.
- If the output will be saved, hand off the final result to `research-note-wrap`.
