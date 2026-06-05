---
name: workflow-creator-deep
type: variation
variant: deep
---

# Workflow Creator Deep Mode

Use when the workflow coordinates multiple agents, skills, handoffs, or failure
routes. Load only relevant local assets and existing local context:

- `assets/activation-policy.json`
- `assets/workflow-definition-contract.json`
- `assets/quality-gates.json`
- `assets/workflow-output-template.md`
- owning skill files, if present

Do not bulk-load nonexistent `references/` directories. Keep every claim
evidence-tagged, mark unresolved catalog references `[OPEN]`, and run the local
validator when JSON workflow input is available.
