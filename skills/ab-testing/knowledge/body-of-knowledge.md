# Ab Testing — Body of Knowledge

## Canon

A/B testing compares a control and one or more variants against a predefined
decision rule. The purpose is not to "get significance"; the purpose is to make
a product, growth, UX, or content decision with controlled uncertainty.

## Minimum Experiment Contract

| Element | Required Question |
|---|---|
| Decision | What decision will this experiment unlock? |
| Hypothesis | If we change X for audience Y, metric Z will move by N because R. |
| Control | What current experience or behavior remains unchanged? |
| Variant | What exactly changes, and where can a reviewer inspect it? |
| Primary metric | Which single metric decides the outcome? |
| Guardrails | Which metrics must not degrade? |
| Population | Which users, sessions, geographies, devices, or accounts are eligible? |
| Exposure | How is assignment logged and kept stable? |
| MDE | What minimum detectable effect is worth acting on? |
| Power/significance | What power and alpha threshold are assumed? |
| Duration | How long must the test run to cover weekly cycles and required sample? |
| Decision rule | What happens on win, loss, inconclusive, guardrail harm, or bad data? |

## Readiness States

| State | Meaning | Next Action |
|---|---|---|
| Ready | Hypothesis, metric contract, traffic, instrumentation, and decision rule are complete. | Launch with monitoring. |
| Blocked | Required data or ownership is missing. | Collect missing inputs before traffic is spent. |
| Risky | Test can run but has validity threats. | Mitigate or document accepted risk. |
| Invalid | Current design cannot answer the decision. | Redesign or use a different research method. |

## Common Validity Threats

| Threat | Why It Matters | Mitigation |
|---|---|---|
| Peeking | Early stopping can inflate false positives. | Define monitoring and stopping policy before launch. |
| Sample ratio mismatch | Uneven assignment may indicate broken randomization or logging. | Check exposure counts by variant before analysis. |
| Seasonality | Weekday, campaign, or holiday effects can skew behavior. | Run through complete business cycles when feasible. |
| Overlapping experiments | Concurrent tests can contaminate effects. | Segment, sequence, or document interactions. |
| Instrumentation drift | Event changes break comparability. | Freeze event definitions and validate payloads. |
| Novelty effect | Short-term behavior may not reflect stable adoption. | Monitor guardrails and consider follow-up retention checks. |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Experiment-contract completeness | 100% for launch-ready recommendation | Required fields present or marked blocked |
| Evidence coverage | 100% | Claims tagged with evidence, assumption, or open requirement |
| Decision clarity | 100% | Win/loss/inconclusive/guardrail-failure actions named |
| Validity threat coverage | >= 5 relevant threats considered | Risk section names threat and mitigation |

## References
- Related internal skills: `analytics-events`, `funnel-analytics`,
  `conversion-optimization`, `data-validation`.
- Use external statistical or experimentation standards only when a task requires
  formal methodology or publication-grade claims.
