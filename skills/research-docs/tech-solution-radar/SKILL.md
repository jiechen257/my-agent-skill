---
name: tech-solution-radar
description: Research and compare technical solutions or product competitors to support a selection or product-improvement decision. Use for framework, library, architecture, tool or SaaS selection, industry best practices, and evidence-backed competitor experience, positioning and differentiation analysis.
---

# tech-solution-radar

Turn research into a decision supported by traceable evidence. Preserve the user's goal: choosing a solution and learning from competitors require different conclusions, even when they concern the same products.

## Choose the branch

Choose by the decision the user needs, rather than by whether the candidates are libraries, tools or SaaS products.

| Decision | Branch | Read before analysis | Deliverable |
| --- | --- | --- | --- |
| Which solution should we adopt, buy or integrate? What technical practice should we follow? | Technical selection | [Technical selection](references/technical-selection.md) | Recommendation, fit, tradeoffs and adoption risks |
| How do competitors serve users, and what should our product learn or improve? | Product competitor analysis | [Product competitor analysis](references/competitive-analysis.md) | Task and experience comparison, differentiation and testable opportunities |
| Both adoption and product-improvement decisions are requested | Mixed | Both references | Shared evidence, separate selection and product recommendations |

Load only the reference needed for the chosen branch. For a mixed task, keep procurement or integration suitability separate from product lessons; one product can be a poor adoption choice and still provide a useful design example.

## Inputs

| Input | Meaning |
| --- | --- |
| `topic` | Problem, category or products to investigate |
| `scenario` | Intended users, user task, environment, stack, scale and constraints |
| `decision` | What the user needs to choose or improve; infer the branch from this |
| `must_have` | Hard requirements and exclusion rules |
| `nice_to_have` | Preferences that influence the recommendation |
| `time_window` | Recency scope; use current evidence unless a historical comparison is requested |
| `output_depth` | `quick`, `standard` or `deep`; default to `standard` |

Use context already provided. Ask at most one clarification question when the missing goal or constraints would materially change the recommendation; otherwise state a reasonable assumption and continue. Respect named candidates and the requested depth.

## Shared workflow

1. **Frame the decision.** Identify the user task, branch, baseline, hard constraints and comparison criteria. For product improvement, establish the user's current product or workflow as the baseline when evidence is available; otherwise label it unknown.
2. **Build a relevant candidate set.** Include direct substitutes first, then indirect alternatives or emerging competitors when they can change the decision. Expand discovery as needed; keep a user-specified shortlist intact.
3. **Collect and verify evidence.** Prefer official documentation, source repositories, release notes, pricing and plan pages for documented capabilities. Use authorized hands-on observations for experience claims, and community feedback for reported issues and adoption signals. Verify time-sensitive facts live unless the task is explicitly limited to supplied or historical material; state that boundary when it limits the conclusion.
4. **Analyze with the selected reference.** Apply its criteria to comparable evidence. Preserve unknowns and distinguish established findings from hypotheses. Select scoring, qualitative tiers or a comparison matrix according to evidence quality and the decision.
5. **Recommend and bound the conclusion.** Lead with what to adopt or improve and why. Link material findings to their sources, explain tradeoffs and evidence gaps, state confidence based on evidence coverage, and identify the next validation that could change the decision.

## Evidence rules

- Label material claims as **documented** (officially stated), **observed** (actually exercised), **reported** (third-party feedback) or **inferred** (analysis). An official feature claim alone supports availability as documented, not observed usability, reliability or performance.
- Record the source and evidence date. For context-sensitive claims, also identify the version, platform, plan or configuration. Keep conflicting observations attached to their contexts instead of flattening them into one verdict.
- Compare the same user task and success condition. Record completion, output quality, failure recovery and user effort where evidence permits. Use comparable conditions for measured performance claims.
- Use existing authorized access. Unavailable access or an unexecuted test is an evidence gap: label it **unverified**, rather than calling the feature absent or defective.
- Preserve hard gates. A failed requirement excludes an adoption candidate; an unverified requirement makes adoption conditional on verification. Popularity or a weighted total cannot override either status.
- Separate facts, inferences and preferences. Missing data stays unknown, and weak evidence calls for a qualified conclusion rather than invented numbers or a precise ranking.

## Output and completion

Use Simplified Chinese by default. Match detail to the requested decision and depth, using the selected reference's output guidance. Quick research may remain qualitative; deep research should include the evidence needed to inspect each material comparison.

Before finishing, check that:

- the conclusion answers the selected decision, including both decisions in mixed mode;
- adoption recommendations account for every hard requirement, including unknown ones;
- important claims have sources and appropriate evidence labels and context;
- experience or performance claims reflect the actual observations available;
- product recommendations identify their baseline, expected user benefit and a way to validate the improvement;
- remaining gaps and conditions that could change the recommendation are explicit.

When the user requests a saved research note, use `research-note-wrap` if available and follow the requested destination and format. Otherwise deliver the findings in chat.
