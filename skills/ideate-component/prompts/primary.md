---
name: ideate-component-primary
type: execution
version: 2.0.0
description: "Execute the Ideate Component workflow."
triad:
  lead: "ideate-component-lead"
  support: "ideate-component-support"
  guardian: "ideate-component-guardian"
---

# Ideate Component - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Confirm the request asks for one plugin component concept, not a full implementation.
2. Identify component type: skill, agent, command, or hook.
3. Read `references/component-patterns.md` and relevant plugin files if a path is provided.
4. Inventory existing components and their names before proposing candidates.
5. Produce 2-3 kebab-case candidates, one recommendation, relationships, conflicts, MOAT depth, tools, line range, validation, and risks.
6. Validate against `assets/concept-card-contract.json` before delivering.
