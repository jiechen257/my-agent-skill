---
name: forward-deployed-engineer
description: "Use when evaluating or delivering enterprise AI work as an FDE: discovering the real workflow, selecting a valuable problem, auditing a codebase or roadmap for 增值区/贬值区 investments, defining a minimum viable deployment, activating adoption, protecting renewal, expanding value, or turning field solutions into reusable product capabilities."
---

# Forward Deployed Engineer

Turn field reality into measurable customer value, then turn repeated delivery learning into reusable product leverage. Treat the field as the probe, the platform as the lever, and the product as the compounding asset.

## Select the branch

- **Investment audit**: inspect a codebase, architecture, roadmap, workflow, or AI initiative and classify its 增值区、贬值区、控制面与通用底座. Read [value-zone-audit.md](references/value-zone-audit.md).
- **New engagement**: discover the real problem, establish PSF, and define an MVD. Read [field-delivery-loop.md](references/field-delivery-loop.md) through “Minimum viable deployment”.
- **Active deployment**: diagnose activation, reliability, adoption, renewal, or expansion. Read the relevant later phases in [field-delivery-loop.md](references/field-delivery-loop.md) and use [metrics-and-ethics.md](references/metrics-and-ethics.md).
- **Scale and productize**: extract playbooks, components, platform capabilities, and product signals from repeated field work. Read “Compound field learning” in [field-delivery-loop.md](references/field-delivery-loop.md).

For mixed requests, run the common workflow below and load each reference only when its branch begins.

## 1. Establish the field boundary

State the customer, users, business process, environment, desired outcome, time horizon, and decision this run must support. Distinguish direct evidence, inference, and unknowns.

Use the live surface as the acceptance boundary: inspect current code and configuration, but also inspect available runtime state, data, tests, logs, deployment records, user behavior, and stakeholder artifacts. Do not infer production value from architecture diagrams or feature presence alone.

Completion criterion: the target decision and the evidence surfaces that can prove it are explicit.

## 2. Reconstruct the real work

Follow the work rather than the official process. Identify:

- the user with the pain and the person who owns the result;
- the trusted data source and hidden data workarounds;
- the actual steps, exceptions, handoffs, and shadow workflows;
- the systems, permissions, compliance, and release constraints;
- the supporters, veto holders, knowledge hubs, and threatened roles.

For a repository audit, translate these into concrete modules and call paths. Separate what merely exists from what an agent can actually call and verify.

Completion criterion: the critical workflow, source of truth, owner, blocking environment, and verification signal are evidenced or marked unknown.

## 3. Decide whether the problem deserves deployment

Test Problem-Solution Fit on three axes:

1. **Pain**: a specific person experiences a costly, repeated problem.
2. **Economics**: baseline time, cost, risk, revenue, or quality loss can be measured.
3. **Feasibility**: real data, access, accuracy threshold, and operational constraints make a useful result possible.

Reject or defer when there is no business owner, no access to representative real data, no measurable graduation criterion, or a first engagement demands organization-wide scope.

Completion criterion: record `proceed`, `defer`, or `reject`, with the decisive evidence and missing prerequisites.

## 4. Audit the investment portfolio

Apply [value-zone-audit.md](references/value-zone-audit.md) to every material asset or proposed investment. Split mixed modules instead of forcing a folder-level label.

End each item with one action:

- `invest`: deepen an AI-callable environment, verifier, proprietary context, or compounding reusable asset;
- `protect`: retain state, permission, audit, budget, rollback, or high-risk human control;
- `toolify`: move deterministic work or internal routing out of prose and into typed tools or registries;
- `thin`: reduce fixed reasoning order, prompt recipes, markers, retries, and model-specific glue;
- `retire`: stop funding an asset that a stronger model is likely to absorb;
- `observe`: gather missing runtime or customer evidence before deciding.

Completion criterion: every material investment has evidence, a class, a next-model effect, and an action.

## 5. Define the minimum viable deployment

Use representative real data, one end-to-end high-value slice, a week-scale deadline, and a pre-agreed graduation threshold. Reduce breadth, not value density.

Define:

- baseline and target outcome;
- user and workflow boundary;
- required data, integrations, permissions, and rollback;
- machine-verifiable evaluation plus the smallest necessary human judgment;
- `graduate`, `iterate`, and `stop` conditions;
- the owner of each dependency and decision.

Do not call a demo, synthetic-data prototype, or feature-complete sandbox an MVD unless value occurs inside a representative operating environment.

Completion criterion: another team could run the deployment and reach the same go/no-go decision from the written criteria.

## 6. Activate and measure value

Instrument the shortest closed loop from change to feedback: build, test, deploy, exercise the workflow, capture logs and behavior, evaluate, then decide whether to iterate or stop.

Select 3–5 metrics from [metrics-and-ethics.md](references/metrics-and-ethics.md): normally one outcome metric, one adoption metric, one reliability or quality metric, and one relationship or reuse signal. Capture the baseline before intervention.

Treat launch as the start of activation. Track whether target users embed the system into real work, not whether accounts were provisioned.

Completion criterion: the value ledger contains baseline, current result, evidence source, owner, and next intervention.

## 7. Compound field learning

After a deployment or audit, sort learning into three rungs:

1. **Playbook**: judgments, checklists, known traps, metrics, and role maps.
2. **Component**: reusable integrations, evaluators, schemas, adapters, and automation.
3. **Platform**: common capabilities that make recurring work self-service or default.

Promote a field solution only when recurrence and economics justify lifetime maintenance. Track what should remain customer-specific, what should be reused, and what should become product.

Completion criterion: the run leaves a reuse candidate, a named owner, evidence of recurrence, and either a promotion decision or an explicit reason to keep it local.

## 8. Transfer ownership and preserve trust

Apply [metrics-and-ethics.md](references/metrics-and-ethics.md) before handoff. Keep customer data under customer control, report negative results honestly, avoid engineered dependency, account for affected people, reject unsafe requests, and leave the customer able to operate without the FDE.

Completion criterion: operational ownership, access, rollback, documentation, knowledge transfer, unresolved risks, and follow-up measures all have named owners.

## Output contract

Lead with the decision. Use only the sections the selected branch needs:

1. **结论** — proceed/defer/reject or the portfolio judgment.
2. **现场证据** — observed facts, sources, and important unknowns.
3. **PSF 与价值假设** — pain, economics, feasibility, baseline, target.
4. **增值/贬值矩阵** — asset, evidence, classification, next-model effect, action.
5. **MVD 或干预计划** — slice, environment, verifier, threshold, owner, deadline.
6. **价值账本与健康度** — baseline/current/target and evidence source.
7. **复利资产** — playbook/component/platform candidates and retirement list.
8. **风险与下一决策** — not a generic task list; name the decision and its owner.

Default to Simplified Chinese. Keep code identifiers, commands, paths, product keys, and protocol fields unchanged.

## Quality gate

Before finishing, verify:

- the conclusion is tied to current field evidence rather than feature inventory;
- every material asset is classified at the right granularity;
- “AI-callable” claims name the actual callable path and feedback signal;
- proposed value has a baseline, threshold, and owner;
- control-plane work is not mislabeled as prompt debt;
- proprietary knowledge is distinguished from generic prompt technique;
- the next stronger model would amplify the retained investments rather than erase their purpose;
- negative evidence, blocked access, and ethical constraints remain visible.
