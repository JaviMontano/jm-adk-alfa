---
name: ai-workflow-automation-quick
type: variation
version: 2.0.0
description: "Ai Workflow Automation in quick mode."
---

# AI Workflow Automation — quick Mode

## When to Use

Use quick mode when you need adjusted depth for the Ai Workflow Automation workflow.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{context}}` | No | Auto-detected |
| `{{depth}}` | No | Set to "quick" |

## Execution

1. Load skill: `skills/ai-workflow-automation/knowledge/body-of-knowledge.md`
2. Load assets: `assets/manifest.json`, `assets/workflow-schema.json`, and
   `assets/report-contract.json`
3. Execute at quick depth with actor map, step graph, approvals, handoffs,
   bounded retries, and evidence tags
4. Lead → Support → Guardian validation
5. Run offline plan validation when JSON output is produced

## Output

- Deliverable calibrated to quick depth
- Evidence-tagged, Constitution-compliant
- Workflow steps, gates, handoffs, fallbacks, validation, and risks
