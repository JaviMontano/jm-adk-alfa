<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection Output

## Summary

{summary: tool elegido y estrategia aplicada en una frase}

## Evidence

{evidence: matches de Grep/Glob y archivos leidos con Read}

## Result

{result: el Edit o Write aplicado, con anchor unico}

## Validation

{validation: tool coincide con intencion, sin Read masivo upfront, anchor unico, fallback definido}

- Offline validator: `bash skills/katas-builtin-tool-selection/scripts/check.sh`
- Contract assets: `assets/builtin-tool-selection-report-contract.json`, `assets/tool-fit-policy.json`, `assets/read-economy-policy.json`, `assets/edit-anchor-policy.json`, `assets/evidence-policy.json`

## Risks and Limits

{risks: anchors ambiguos pendientes, imports no seguidos, supuestos}

## JSON Report

```json
{
  "schema": "jm-labs.katas-builtin-tool-selection.report.v1",
  "skill": "katas-builtin-tool-selection",
  "objective": "{objective}",
  "scope": "{scope}",
  "selected_strategy": "{selected_strategy}",
  "tool_decisions": "{tool_decisions_json}",
  "read_plan": "{read_plan_json}",
  "edit_plan": "{edit_plan_json}",
  "evidence": "{evidence_json}",
  "validation": "{validation_json}",
  "risks": "{risks_json}"
}
```
