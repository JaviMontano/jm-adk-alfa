---
name: workspace-governance-primary
type: execution
version: 2.0.0
description: "Execute the Workspace Governance workflow with triad orchestration."
triad:
  lead: "workspace-governance-lead"
  support: "workspace-governance-support"
  guardian: "workspace-governance-guardian"
---

# Workspace Governance — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{workspace_inventory}}` | Existing workspace directories and files | Yes | Workspace |
| `{{gitignore_state}}` | Whether `workspace/` is ignored | Yes | Repo |
| `{{tasklog_items}}` | Open tasklog IDs requiring bridges | No | Workspace |
| `{{output_format}}` | md or JSON governance report | No | Auto |

## Execution

1. Confirm request is about `workspace/`, session folders, task bridges, estandares, or gitignored user layer.
2. Inspect `.gitignore`, workspace inventory, and tasklog evidence.
3. Validate root, README coverage, dated sessions, task bridges, and stale-session flags.
4. Propose safe actions under `workspace/` or `.gitignore`.
5. Validate JSON reports with `scripts/check.sh`.

## Output

- Workspace governance report
- Evidence tags on every claim
- Safe action plan
- Guardian pass/block decision
