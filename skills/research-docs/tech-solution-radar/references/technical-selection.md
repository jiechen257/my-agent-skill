# Technical selection

Use for selecting libraries, frameworks, architecture patterns, tools, SaaS products or industry practices. The result should explain what fits the actual scenario and what adoption will cost.

## Candidate discovery and assessment

For broad discovery, aim for 5–10 plausible candidates when that many relevant alternatives exist; a narrow task or named shortlist can be smaller. Favor direct substitutes before adjacent approaches.

Evaluate:

- **Functional fit:** hard requirements, integration shape, extensibility and operating environment.
- **Adoption and ecosystem:** independent usage signals, integrations, documentation and available expertise.
- **Maintenance:** release activity, compatibility, maintainer or vendor stability, issue response and support.
- **Cost and risk:** implementation, migration, operation, pricing, lock-in and learning effort.

Use primary sources for technical capabilities. Popularity can inform ecosystem confidence but does not establish fit or quality. For closed-source SaaS, use relevant vendor, support and integration evidence; for architecture patterns, assess applicability and operational tradeoffs instead of forcing repository metrics.

## Scoring is optional

Use a weighted ranking when candidates have sufficiently comparable evidence and ranking helps the decision. Otherwise present qualitative tiers or a tradeoff table. Material unknowns should be visible as pending checks, rather than converted to zero or guessed scores.

The original weighting remains an available starting point for comparable software options, not a default for every task:

| Dimension | Starting weight | Evidence |
| --- | ---: | --- |
| Functional fit | 45% | Requirements, integration, extensibility, operational fit |
| Popularity/adoption | 25% | Stars, downloads, dependents, community and ecosystem usage |
| Maintenance health | 20% | Releases, compatibility, response and maintainer or vendor stability |
| Implementation risk | 10% | Migration, complexity, lock-in, operation and learning cost |

When using scores, state the scale and weights and link the score rationale to evidence. Adjust the weights for the scenario: long-lived infrastructure may emphasize maintenance and operating risk; a prototype may emphasize fit and implementation effort. Explain the adjustment and normalize volatile metrics rather than comparing raw counts blindly. Higher scores should consistently mean more favorable suitability, including lower risk.

If unavailable evidence could reverse the ranking, use a conditional recommendation and name the missing verification. Small score differences do not justify a strong winner when uncertainty is larger than the difference. Hard requirements remain gates outside the weighted score.

## Adoption signals

Use multiple relevant signals when available:

- Repository stars, forks, contributors, release cadence and issue or PR activity.
- Registry downloads, dependents and version freshness.
- Integrations, plugins, documentation, examples and community activity.
- Official adoption reports, standards and vendor support.

State the snapshot date for time-sensitive numbers. Different metrics measure different populations; neither a star count nor a vendor case study alone proves adoption at the user's scale.

## Output

Lead with the recommended choice or shortlist and its boundary conditions. Include:

1. A comparison table covering requirement status, functional fit, maintenance or support, adoption evidence, cost and risks. Add weights and scores only when justified above.
2. Sources for material claims, with context and evidence gaps.
3. An adoption decision for each serious candidate: suitable now, conditional on a named check, or excluded by a named requirement.
4. The smallest useful pilot or validation that could change the decision.

For a technical best-practice question, compare applicable approaches and explain the conditions under which each works; a product ranking is unnecessary.
