<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-confidence-stratified-sampling
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Confidence Stratified Sampling Output

## Summary

{summary}

## Evidence

{evidence}

## Result

{result}

## Validation

{validation}

- Offline validator: `bash skills/katas-confidence-stratified-sampling/scripts/check.sh`
- Contract assets: `assets/confidence-calibration-report-contract.json`, `assets/calibration-policy.json`, `assets/stratified-sampling-policy.json`, `assets/accuracy-reporting-policy.json`, `assets/routing-policy.json`, `assets/evidence-policy.json`

## Risks and Limits

{risks}

## JSON Report

```json
{
  "schema": "jm-labs.katas-confidence-stratified-sampling.report.v1",
  "skill": "katas-confidence-stratified-sampling",
  "extraction_task": "{extraction_task}",
  "labeled_validation_set": "{labeled_validation_set_json}",
  "calibration": "{calibration_json}",
  "sampling": "{sampling_json}",
  "accuracy_report": "{accuracy_report_json}",
  "routing": "{routing_json}",
  "evidence": "{evidence_json}",
  "validation": "{validation_json}",
  "risks": "{risks_json}"
}
```
