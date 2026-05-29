<!--
generated-by: scripts/scaffold-skill.py
generated-for: ab-testing
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Ab Testing Output

## Summary

{one_paragraph_decision_summary}

## Experiment Contract

| Field | Value |
|---|---|
| Decision to make | {decision} |
| Hypothesis | {hypothesis} |
| Audience / population | {audience} |
| Control | {control} |
| Variant | {variant} |
| Primary metric | {primary_metric} |
| Guardrail metrics | {guardrail_metrics} |
| Data source / events | {data_source_events} |

## Assumptions

| Assumption | Value | Evidence Status |
|---|---|---|
| Baseline | {baseline} | {baseline_evidence_status} |
| MDE | {mde} | {mde_evidence_status} |
| Power | {power} | {power_evidence_status} |
| Significance threshold | {alpha} | {alpha_evidence_status} |
| Traffic per variant | {traffic} | {traffic_evidence_status} |

## Sample Size and Duration

{sample_size_and_duration}

## Launch Checklist

- [ ] Exposure assignment is logged.
- [ ] Event names and payloads are stable.
- [ ] Sample ratio check is defined.
- [ ] Guardrails have alert thresholds.
- [ ] Stopping rule is documented.

## Decision Rule

| Outcome | Action |
|---|---|
| Win | {win_action} |
| Loss | {loss_action} |
| Inconclusive | {inconclusive_action} |
| Guardrail harmed | {guardrail_action} |
| Instrumentation failure | {instrumentation_failure_action} |

## Risks and Mitigations

{risks_and_mitigations}

## Evidence and Open Requirements

{evidence_and_open_requirements}

## Validation Status

{validation_status}
