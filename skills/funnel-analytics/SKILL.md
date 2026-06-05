---
name: funnel-analytics
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Define, audit, and optimize digital conversion funnels with event taxonomy,
  step denominators, drop-off analysis, segment cuts, instrumentation gaps,
  and experiment-ready recommendations. [EXPLICIT]
  Trigger: "funnel analytics", "conversion funnel", "drop-off analysis",
  "activation funnel", "checkout funnel"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Funnel Analytics

> "A funnel is a measurement contract before it is a chart."

## TL;DR

Use this skill to turn product, commerce, onboarding, or acquisition journeys into a deterministic funnel analysis contract: stages, events, denominators, identity/session rules, data quality checks, drop-off interpretation, and testable optimization hypotheses. Do not invent event names, traffic volumes, conversion rates, causal explanations, or experiment results without provided evidence. Mark gaps as `not verified`. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the business goal: acquisition, signup, activation, checkout, retention, or another user journey.
- Capture the funnel unit of analysis: user, account, session, order, lead, or device.
- Inventory available evidence: analytics events, data warehouse tables, BI dashboards, product specs, tracking plans, experiment logs, and source code.
- Map each funnel step to a precise event or state transition, including entry criteria, exit criteria, timestamp, owner, and source.
- Record attribution, identity stitching, timezone, bot/internal-traffic filters, privacy constraints, and known tracking gaps.
- Mark missing instrumentation, formulas, samples, and segments as `not verified` instead of estimating them.

### Step 2: Analyze
- Define formulas before interpreting results: denominator, numerator, conversion rate, drop-off rate, confidence window, cohort window, and exclusion rules.
- Compare counts across steps only when the unit, time window, and deduplication rules match.
- Separate evidence-backed facts from hypotheses. Avoid causal language when only observational funnel data is available.
- Inspect segment cuts such as channel, plan, device, geography, lifecycle stage, experiment bucket, and customer tier when sample size supports it.
- Look for instrumentation risks: duplicate events, missing events, out-of-order timestamps, late-arriving data, identity resets, funnel leakage, and step skipping.
- Prioritize opportunities by impact, confidence, effort, reversibility, and measurement readiness.

### Step 3: Execute
- Produce a funnel definition table with step, event/source, unit, denominator, numerator, exclusions, owner, and evidence status.
- Produce a drop-off table only from verified counts or explicitly label sample/proxy data.
- Add data-quality notes for every weak or missing measurement dependency.
- Convert findings into optimization hypotheses with required instrumentation, target metric, guardrail metrics, and validation method.
- Recommend experiments, instrumentation fixes, or research follow-ups according to evidence strength.
- When code or analytics configs are available, point to exact files/tables/events inspected.

### Step 4: Validate
- Confirm every quantitative claim has a source, sample window, unit, and denominator.
- Confirm recommendations do not depend on unverified tracking.
- Confirm privacy-sensitive data is minimized and no direct personal identifiers are exposed in the deliverable.
- Confirm the deliverable follows `assets/deliverable-checklist.md`.
- If the repository includes scripts for the skill, run its check script and `validate-skill-scripts.py --strict --run-checks --skill funnel-analytics`.

## Quality Criteria

- [ ] Funnel objective, audience, unit, time window, and data owner are explicit.
- [ ] Every step has an event/source mapping and evidence status.
- [ ] Denominators, numerators, exclusions, and deduplication rules are documented before rates are interpreted.
- [ ] Data-quality gaps are marked `not verified` and not filled with invented assumptions.
- [ ] Segment analysis includes sample-size and comparability cautions.
- [ ] Recommendations are separated into instrumentation fixes, research tasks, product changes, and experiments.
- [ ] Causal claims are avoided unless supported by experimental or quasi-experimental evidence.
- [ ] Privacy, PII, consent, and retention constraints are respected.
- [ ] Evidence tags are applied to all claims.

## Anti-Patterns

- Treating a dashboard screenshot as enough evidence for event definitions.
- Comparing step counts with different units, windows, or deduplication rules.
- Claiming "users drop because of friction" without session replay, research, experiment, or product evidence.
- Recommending conversion tactics before the tracking plan is reliable.
- Hiding uncertainty in averages when segment or cohort effects may reverse the conclusion.
- Logging or displaying direct personal identifiers when aggregate metrics are sufficient.

## Output Contract

The default output is a concise Markdown report with:

- scope and evidence inventory
- funnel definition table
- metric formulas and denominator rules
- drop-off and segment analysis
- instrumentation and data-quality gaps
- optimization hypotheses and experiment backlog
- validation plan, privacy notes, and residual risks

## Usage

Example invocations:

- "/funnel-analytics" - Run the full funnel analytics workflow
- "analyze signup-to-activation drop-off from these events" - Build a verified funnel analysis
- "audit our checkout funnel tracking plan" - Check instrumentation before recommending optimization


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Uses the language of the user request unless repo conventions require otherwise [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- Does not certify analytics accuracy unless source data, tracking plan, and validation checks were inspected or provided [EXPLICIT]
- Does not create or mutate product instrumentation when the user asks only for analysis/specification [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce a minimum viable tracking brief and ask for events, counts, and business goal |
| Counts without event definitions | Treat rates as provisional and request/source event taxonomy |
| Mixed units or time windows | Stop rate comparison until denominators are reconciled |
| Small sample or rare conversion | Prefer instrumentation/research next step over optimization claims |
| Conflicting dashboard values | Flag discrepancy, list likely causes, and request source-of-truth owner |
| Out-of-scope request | Redirect to appropriate skill or escalate |

## Assets

- `assets/deliverable-checklist.md` provides the reusable checklist for final deliverable and guardian review.
