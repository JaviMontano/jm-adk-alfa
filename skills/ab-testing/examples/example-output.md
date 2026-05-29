<!--
generated-by: scripts/scaffold-skill.py
generated-for: ab-testing
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Readiness: risky until instrumentation and stopping policy are confirmed. [EXPLICIT]
The test idea is valid because it maps one headline change to one primary signup metric, but the team must define exposure logging, sample ratio checks, and stop rules before traffic starts. [EXPLICIT]

## Experiment Contract

| Field | Value |
|---|---|
| Decision | Ship the new headline, keep the control, or run a follow-up test. |
| Hypothesis | If paid-search visitors see the workflow-specific headline, completed trial signup will increase by at least 10% relative because the value proposition becomes more concrete. [ASSUMPTION] |
| Audience | New paid-search visitors in the United States. |
| Control | "Start your free trial" hero headline. |
| Variant | "Launch your first workflow in 10 minutes" hero headline. |
| Primary metric | Completed trial signup. |
| Guardrails | Demo requests, support tickets, bounce rate. |

## Sample Size and Duration

Baseline, MDE, and traffic are present, so the next step is a formal calculator or statistical script using the agreed alpha and power. [EXPLICIT]
Do not launch until alpha, power, and business-cycle coverage are selected. [EXPLICIT]

## Launch Checklist

- [ ] Confirm event name for exposure assignment.
- [ ] Confirm event name for completed trial signup.
- [ ] Define sample ratio mismatch check.
- [ ] Define guardrail alert thresholds.
- [ ] Define stop rule before launch.

## Decision Rule

| Outcome | Action |
|---|---|
| Win | Ship only if primary metric meets the preselected threshold and guardrails stay healthy. |
| Loss | Keep control and document learning. |
| Inconclusive | Do not ship by default; decide whether MDE was too ambitious or traffic too low. |
| Guardrail harmed | Pause rollout even if primary metric improves. |
| Instrumentation failure | Invalidate the test and relaunch after fixing logging. |

## Risks

- Peeking risk if the team checks daily and stops early.
- Seasonality risk if the test does not cover a full weekly cycle.
- Instrumentation drift risk if signup events change during the campaign.

## Validation

- Skill activated intentionally for A/B test design.
- Output follows the experiment brief format.
- Risks and assumptions are explicit.
