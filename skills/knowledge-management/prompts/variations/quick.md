---
name: knowledge-management-quick
type: variation
version: 2.0.0
description: "Knowledge Management in quick mode."
---

# Knowledge Management — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Knowledge Management workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/knowledge-management/knowledge/body-of-knowledge.md`
2. Load assets: `assets/manifest.json` and `assets/report-contract.json`
3. Execute at quick depth with evidence tags, source paths, owners, retrieval
   terms, and explicit `reference_date`
4. Lead → Support → Guardian validation
5. Run offline report validation when JSON output is produced

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Register, gaps, actions, risks, and validation notes
