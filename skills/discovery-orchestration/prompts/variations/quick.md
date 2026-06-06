---
name: discovery-orchestration-quick
type: variation
version: 2.0.0
description: "Discovery Orchestration in quick mode."
---

# Discovery Orchestration — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Discovery Orchestration workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/discovery-orchestration/knowledge/body-of-knowledge.md`
2. Load assets: `assets/manifest.json` and `assets/report-contract.json`
3. Execute at quick depth with phases, dependencies, gates, deliverables,
   blockers, and evidence tags
4. Lead → Support → Guardian validation
5. Run offline packet validation when JSON output is produced

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Pipeline, gates, deliverables, blockers, validation, and risks
