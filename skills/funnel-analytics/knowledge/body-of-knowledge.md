# Funnel Analytics - Body of Knowledge

## Canon

Funnel analytics is useful only when the measurement contract is explicit. A valid funnel defines the objective, step order, unit of analysis, event sources, denominator rules, exclusions, identity/session handling, and time window before interpreting conversion or drop-off.

## Core Contracts

| Contract | Required Decision |
|---|---|
| Objective | What user/business outcome the funnel explains |
| Unit | User, account, session, order, lead, device, or another stable entity |
| Step | Event/state, entry criteria, exit criteria, timestamp, owner, and source |
| Denominator | Which population enters each step and which exclusions apply |
| Window | Date range, timezone, cohort window, and late-arriving data rule |
| Identity | Anonymous/authenticated stitching, dedupe, retries, and resets |
| Segment | Channel, plan, geography, device, lifecycle, experiment bucket, or tier |
| Quality | Missing events, duplicates, out-of-order events, data freshness, and owner |
| Privacy | PII minimization, consent constraints, retention, and aggregation threshold |

## Interpretation Rules

- Define formulas before calculating rates.
- Compare counts only when unit, time window, source, and deduplication rules match.
- Distinguish facts, hypotheses, and recommendations.
- Avoid causal language without experiment, research, or causal design evidence.
- Treat segment analysis as provisional when sample sizes are small or cohorts differ.
- Prefer instrumentation fixes over optimization recommendations when tracking is unreliable.
- Report uncertainty plainly: `not verified`, `sample only`, `proxy metric`, or `needs source owner`.

## Common Failure Modes

- Event names exist but payloads lack required properties.
- Step counts mix sessions and users.
- Dashboard totals use rolling windows while export data uses fixed cohorts.
- Duplicate submissions inflate conversion.
- Identity resets split one user across anonymous and authenticated IDs.
- Late-arriving data creates apparent drop-off in recent cohorts.
- Segment mix hides the real pattern or reverses the aggregate conclusion.
- Teams optimize an uninstrumented step and cannot prove impact.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---------------|
| Evidence coverage | 100% | Every metric, event, and recommendation cites source or says `not verified` |
| Definition completeness | 100% | Every funnel step has source, unit, denominator, and owner |
| Formula clarity | 100% | Conversion/drop-off formulas define numerator, denominator, and exclusions |
| Data-quality coverage | 100% | Missing/duplicate/out-of-order/freshness risks considered |
| Privacy coverage | 100% | PII, consent, aggregation, and retention constraints documented |

## References

- Analytics tracking plans and event taxonomies from the active project
- Product analytics source tables, BI dashboards, or instrumentation configs
- Experiment design notes, A/B test logs, and product research artifacts
- Privacy policies, consent rules, and data-retention requirements
