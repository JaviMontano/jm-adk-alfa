---
name: ai-architecture-implementation-primary
type: execution
version: 2.0.0
description: "Execute the AI Architecture Implementation workflow."
triad:
  lead: "ai-architecture-implementation-lead"
  support: "ai-architecture-implementation-support"
  guardian: "ai-architecture-implementation-guardian"
---

# AI Architecture Implementation — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system}}` | AI system or roadmap to implement | Yes | User input |
| `{{architecture}}` | Approved design, audit findings, or target state | Yes | User/workspace |
| `{{constraints}}` | Stack, infra, budget, team, compliance | No | User/workspace |

## Execution Steps
1. Confirm implementation-not-audit/design intent.
2. Load assets and relevant references.
3. Build prerequisite and evidence inventory.
4. Produce F0-F5 phased plan with DoD.
5. Capture technology decisions and ADR needs.
6. Include CI/CD, rollback, monitoring, and runbooks.
7. Validate JSON packet with `scripts/check.sh` when present.
