---
name: xlsx-template-creator-primary
type: execution
version: 2.0.0
description: "Execute the deterministic XLSX template specification workflow."
triad:
  lead: "xlsx-template-creator-lead"
  support: "xlsx-template-creator-support"
  guardian: "xlsx-template-creator-guardian"
---

# XLSX Template Creator -- Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{template_type}}` | `tracking-matrix` or `metrics-dashboard` | Yes | User or classifier |
| `{{title}}` | Workbook title | Yes | User |
| `{{locale}}` | Locale for labels and dates | No | User or default |
| `{{columns_or_kpis}}` | Required fields, formulas, KPI names, targets, thresholds | Yes | User/context |
| `{{renderer}}` | Downstream XLSX renderer name | No | User or default |

## Execution

1. Read `SKILL.md`, `assets/xlsx-template-schema.json`, `assets/template-policy.json`, and `assets/formula-policy.json`.
2. Normalize the user request into a workbook JSON spec.
3. Run `scripts/compile-xlsx-template.py` against the spec.
4. Fix validation errors before returning any final workbook contract.
5. Return Markdown for human review or YAML-like output for renderer handoff.
