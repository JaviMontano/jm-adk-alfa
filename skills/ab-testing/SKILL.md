---
name: ab-testing
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Designs and reviews A/B tests with explicit hypothesis, primary metric,
  guardrail metrics, variants, sample-size assumptions, duration, stopping
  rules, instrumentation checks, and decision criteria. [EXPLICIT]
  Trigger: "ab testing, a/b test, experiment design, split test, hypothesis formulation, statistical significance, sample size calculation, test duration"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Ab Testing

> "Method over hacks. Evidence over assumption."

## TL;DR

Designs or audits an A/B test so a team can decide whether to run, fix, stop,
or interpret an experiment without confusing speed with evidence. [EXPLICIT]
The skill must make the hypothesis, metric contract, assumptions, sample-size
needs, duration, instrumentation, risks, and decision rule explicit. [EXPLICIT]

## Procedure

### Step 1: Discover
- Identify the experiment goal, decision owner, user segment, traffic source,
  current baseline, candidate variant, and business constraint. [EXPLICIT]
- Capture the primary metric, guardrail metrics, minimum detectable effect
  (MDE), desired power, significance threshold, and acceptable runtime. [EXPLICIT]
- Inspect existing analytics, event names, funnel definitions, docs, or code
  when available. If they are missing, mark the gap instead of inventing
  metrics. [EXPLICIT]

### Step 2: Analyze
- Convert the idea into a falsifiable hypothesis:
  "If we change X for audience Y, metric Z will move by N because R." [EXPLICIT]
- Check whether an A/B test is appropriate or whether discovery, analytics
  cleanup, usability testing, or a feature flag rollout is safer first. [EXPLICIT]
- Estimate sample-size and duration qualitatively or quantitatively from the
  provided baseline, traffic, variance, MDE, power, and significance inputs.
  If any required input is absent, return a requirements gap and a formula-ready
  checklist. [EXPLICIT]
- Identify validity threats: novelty effects, peeking, seasonality, sample ratio
  mismatch, overlapping experiments, instrumentation drift, and segment bias.
  [EXPLICIT]

### Step 3: Execute
- Produce an experiment brief with hypothesis, variants, metric contract,
  sample-size assumptions, duration recommendation, launch checklist,
  monitoring plan, and decision rule. [EXPLICIT]
- If asked to review an existing test, classify it as ready, blocked, risky,
  or invalid, and name the blocking evidence. [EXPLICIT]
- Keep implementation recommendations scoped to the experiment; route broader
  funnel or analytics work to related skills when needed. [EXPLICIT]

### Step 4: Validate
- Verify that the primary metric has one owner and one definition. [EXPLICIT]
- Verify that every recommendation is tied to provided evidence, an explicit
  assumption, or an open data requirement. [EXPLICIT]
- Verify that the decision rule says what happens for win, loss, inconclusive,
  harmed guardrail, and instrumentation failure outcomes. [EXPLICIT]
- Do not claim statistical significance, lift, ROI, or causality unless the
  required data and method are available. [EXPLICIT]

## Quality Criteria

- [ ] Hypothesis is falsifiable and names change, audience, metric, expected
      movement, and rationale.
- [ ] Primary metric, guardrail metrics, event names, and data source are defined
      or explicitly marked as missing.
- [ ] Sample-size, MDE, power, significance, and duration assumptions are stated;
      absent inputs are listed as blocking requirements.
- [ ] Launch, monitoring, stopping, and decision rules are actionable.
- [ ] Risks include at least peeking, seasonality, overlapping experiments,
      sample ratio mismatch, and instrumentation drift when relevant.
- [ ] Claims use evidence tags or are marked as assumptions/open questions.

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Testing without a decision rule | Produces data but no decision | Define win, loss, inconclusive, and guardrail-failure actions before launch |
| Optimizing many primary metrics | Inflates false positives and weakens accountability | Choose one primary metric and separate guardrails |
| Peeking and stopping early | Makes confidence claims unreliable | Define monitoring and stopping policy before launch |
| Missing instrumentation checks | Invalidates results after traffic is spent | Verify events, exposure logging, and sample ratio before analysis |
| Treating significance as business value | A statistically detectable lift may be too small to matter | Include MDE and practical impact threshold |

## Related Skills

- `analytics-events`
- `funnel-analytics`
- `conversion-optimization`
- `data-validation`
- `experimentation-strategy`

## Usage

Example invocations:

- "/ab-testing" — Run the full ab testing workflow
- "ab testing on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
- If baseline conversion, traffic, variance, or MDE are missing, this skill can
  produce a readiness brief but not a reliable sample-size claim. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
