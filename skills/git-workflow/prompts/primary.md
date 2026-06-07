---
name: git-workflow-primary
type: execution
version: 2.0.0
description: "Execute the Git Workflow workflow with triad orchestration."
triad:
  lead: "git-workflow-lead"
  support: "git-workflow-support"
  guardian: "git-workflow-guardian"
---

# Git Workflow - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |
| `{{depth}}` | quick / standard / deep | No | Auto |
| `{{output_format}}` | html / docx / xlsx / md | No | Auto |

## Execution

1. Read repo state before proposing commands: status, branch, base alignment, and open PRs.
2. Select operation type: feature PR, hotfix, release tag, conflict resolution, or workflow audit.
3. Produce an ordered command plan with preconditions, expected outcomes, rollback notes, and validation commands.
4. Apply command policy: block forbidden destructive commands and unsafe force pushes.
5. Apply branch, PR, conflict, and release policies.
6. Guardian validates against `assets/workflow-plan-contract.json` before delivery.

## Output

- Git workflow plan with evidence tags, stop conditions, and validation checklist.
