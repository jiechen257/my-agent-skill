# Product competitor analysis

Use when the user wants to understand competing products and improve their own product, positioning or user workflow. Analyze the target user and task before comparing feature lists.

## Select competitors and establish a baseline

Start from the user's current product or workflow, its intended users and the problem to improve. Preserve its observed strengths as well as its gaps. If baseline evidence is unavailable, label opportunities as hypotheses and identify what must be checked locally.

Select candidates for what they reveal:

- **Direct competitors:** serve similar users with a similar product or workflow.
- **Indirect alternatives:** solve the same user problem through a different workflow, including manual or existing tools when relevant.
- **Potential competitors:** could plausibly serve the same need; distinguish announced plans from currently available capabilities.

For broad research, 3–5 representative candidates are usually a useful starting point. Follow a named shortlist and expand it only when an omitted alternative could materially change the conclusion.

## Compare a shared user task

Define the task, input, expected output and success condition. Select the journey segments relevant to the decision:

| Dimension | What to investigate |
| --- | --- |
| Entry and onboarding | How users discover the capability, gain access and reach first value |
| Core workflow | Steps, required inputs, user decisions, handoffs and output usefulness |
| Failure and recovery | Visible state, actionable errors, retry, cancel, resume and retained work |
| User effort and performance | Interaction effort, waiting and responsiveness under comparable conditions |
| Positioning | Target users, job to be done, value proposition and differentiation |
| Commercial availability | Plan restrictions, quotas, pricing basis and access to the compared workflow |

Apply the entrypoint's evidence rules to each finding. A release note can establish a documented feature; an observed workflow can establish what happened in the recorded conditions. Neither licenses a general reliability claim from one successful run. User reviews supply reported experiences whose representativeness must be assessed.

Compare documented capabilities separately when hands-on access is unavailable. Keep version, platform, plan and configuration differences visible, and identify the experience checks still needed.

## Turn differences into opportunities

For each material finding, connect:

**Finding → evidence → effect on our target users → proposed change → validation.**

Explain which baseline gap the proposal addresses and the expected benefit. Consider its fit with the product's positioning, implementation or operating cost and tradeoffs. A competitor's feature is a candidate lesson, not sufficient reason to add that feature locally.

Use SWOT only when it clarifies positioning, with each material assertion backed by evidence or labeled as a hypothesis. Porter's five forces is optional for industry structure; value-chain analysis is optional for where value and costs accumulate. A focused workflow comparison may need none of these frameworks.

## Output

Lead with the product lessons and recommended action, then provide:

- The target user/task, baseline and observation scope.
- A comparison matrix with relevant journey, positioning and commercial dimensions, evidence labels and sources. Numeric overall scores are optional and require explicit criteria and comparable evidence.
- Prioritized opportunities, each tied to a finding, expected user benefit, tradeoff and validation method. Example validation: measure recovery completion and repeated user input after an interrupted task, rather than counting whether a retry button exists.
- Unverified claims, competing explanations and the next evidence needed. Tie adoption of a proposed change to an observable acceptance condition when possible.

For mixed research, share the evidence with the technical-selection branch but keep product-improvement recommendations distinct from the choice of what to buy or integrate.

## Source and local adaptation

Adapted from Taylor Chen's [competitive-analysis framework](https://github.com/TaylorChen/super-skills/blob/39c241820a7f0e378f2eb52b887ea44a78242f6e/skills/competitive-analysis/references/analysis-framework.md) in `TaylorChen/super-skills`, commit `39c241820a7f0e378f2eb52b887ea44a78242f6e`, under the [MIT license](../LICENSE.super-skills).

The local adaptation retains competitor classification, workflow observation, positioning, commercial analysis and actionable recommendations. It makes the strategy frameworks optional and adds baseline, evidence-context and validation requirements. It is maintained here as reference material, not installed as a separate upstream skill.
