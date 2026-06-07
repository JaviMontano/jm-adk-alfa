# Analytics Implementation

Use this skill to plan and validate GA4/Firebase Analytics implementation work: setup, custom events, conversions, user properties, BigQuery export, Looker Studio readiness, privacy controls, and QA.

## Trigger Signals

- GA4 or Firebase Analytics setup.
- Custom events, event parameters, conversions, audiences, or user properties.
- BigQuery export, retention, dataset ownership, or analytics warehouse handoff.
- Looker Studio dashboard data sources and metric readiness.
- DebugView, event QA, consent mode, or privacy-safe rollout.

## Deliverable

The skill produces an implementation package with GA4 setup, event contracts, conversions, user properties, BigQuery export, dashboard plan, implementation steps, validation checks, assumptions, and risks.

## Assets And Scripts

`assets/` contains the deterministic policy files. `scripts/check.sh` validates JSON fixtures offline by accepting valid implementation plans and rejecting missing evidence, bad event names, unknown conversions, unsafe user properties, disabled exports, dashboard gaps, and incomplete validation.
