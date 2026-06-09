<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Adaptive Investigation Output

## Summary

{summary}

## Topologia mapeada (Fase 1)

{topology}

## Plan priorizado (Fase 2)

{prioritized_plan}

## Hallazgos del deep-dive (Fase 3)

{findings}

## Re-planes disparados

{replans}  <!-- cada uno: hallazgo que invalido + nuevo orden; vacio si no hubo -->

## Presupuesto

- Archivos: {files_used} / {files_budget}
- Queries: {queries_used} / {queries_budget}
- Estado: {budget_status}  <!-- completo | agotado con pendientes -->

## Evidence

{evidence}

## Validation

{validation}

- Offline validator: `bash skills/katas-adaptive-investigation/scripts/check.sh`
- Contract assets: `assets/adaptive-investigation-report-contract.json`, `assets/exploration-budget-policy.json`, `assets/replan-gate-policy.json`, `assets/evidence-policy.json`, `assets/scratchpad-policy.json`

## Risks and Limits

{risks}

## JSON Report

```json
{
  "schema": "jm-labs.katas-adaptive-investigation.report.v1",
  "skill": "katas-adaptive-investigation",
  "objective": "{objective}",
  "scope": "{scope}",
  "hypothesis": "{hypothesis}",
  "budget": "{budget_json}",
  "topology": "{topology_json}",
  "prioritized_plan": "{prioritized_plan_json}",
  "findings": "{findings_json}",
  "replans": "{replans_json}",
  "scratchpad": "{scratchpad_json}",
  "evidence": "{evidence_json}",
  "validation": "{validation_json}",
  "risks": "{risks_json}"
}
```
