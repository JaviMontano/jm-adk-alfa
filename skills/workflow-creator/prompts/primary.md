---
name: workflow-creator-primary
type: execution
version: 2.1.0
description: "Execute the Workflow Creator contract."
triad:
  lead: "workflow-creator-lead"
  support: "workflow-creator-support"
  guardian: "workflow-creator-guardian"
---

# Workflow Creator Primary Prompt

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{workflow_request}}` | User request and desired workflow outcome | Yes | User input |
| `{{owning_skill_id}}` | Owning skill or `[OPEN]` | Yes | User or local catalog |
| `{{local_context}}` | Existing files, agents, commands, or constraints | No | Workspace |

## Execution Steps

1. Confirm activation using `assets/activation-policy.json`.
2. Ask for missing blocking inputs or mark non-blocking unknowns `[OPEN]`.
3. Load `assets/workflow-definition-contract.json`,
   `assets/quality-gates.json`, and `assets/workflow-output-template.md`.
4. Produce the 17-field workflow spec with 3-7 ordered steps.
5. Validate against `## Validation Gate` in `SKILL.md`.
6. If a JSON spec exists, run `scripts/validate_workflow_spec.py`.
7. Return evidence-tagged activation decision, workflow spec, validation
   evidence, and open risks.
