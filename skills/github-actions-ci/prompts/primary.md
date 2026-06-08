---
name: github-actions-ci-primary
type: execution
version: 2.0.0
description: "Execute deterministic GitHub Actions CI/CD workflow planning."
triad:
  lead: "github-actions-ci-lead"
  support: "github-actions-ci-support"
  guardian: "github-actions-ci-guardian"
---

# GitHub Actions CI/CD - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{repo_surface}}` | Languages, commands, lockfiles, deploy targets, existing workflows | Yes | User or repo evidence |
| `{{workflow_goal}}` | CI, deploy, release, scheduled job, or reusable workflow | Yes | User input |
| `{{constraints}}` | Branch policy, environments, secrets, runners, compliance rules | No | User or repo evidence |
| `{{output_format}}` | md or json | No | Auto |

## Execution

1. Load `knowledge/body-of-knowledge.md`.
2. Load assets under `assets/` and apply policies in this order: contract,
   triggers, permissions, action pinning, cache, matrix, secrets, deployment,
   evidence.
3. Lead: inventory pipeline surface and draft the workflow plan.
4. Support: challenge unsafe triggers, broad permissions, unpinned actions,
   cache invalidation gaps, inline secrets, unbounded matrices, and deploy gates.
5. Guardian: block ready status when any required protection or validation
   evidence is missing.

## Output

- Pipeline Surface
- Triggers
- Jobs
- Permissions
- Actions And Cache
- Matrix
- Secrets And Environments
- Deployment Gates
- Validation Evidence
- Guardian Decision
