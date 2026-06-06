---
name: environment-detection-primary
type: execution
version: 2.0.0
description: "Execute the Environment Detection workflow with triad orchestration."
triad:
  lead: "environment-detection-lead"
  support: "environment-detection-support"
  guardian: "environment-detection-guardian"
---

# Environment Detection — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | Environment or bootstrap decision to make | Yes | User input |
| `{{signals}}` | Local files, tool list, model/context data | Yes | Workspace/runtime |
| `{{constraints}}` | Brand, evidence, persistence, and loading limits | No | User or repo policy |
| `{{depth}}` | quick / standard / deep | No | Risk level |
| `{{output_format}}` | md / json / html / docx | No | User or workflow |

## Execution

1. Read the deterministic policies in `assets/`.
2. Inventory signals and reject network/time/random/account-state evidence.
3. Map IDE to triad mode and context budget to model tier.
4. Build a bounded bootstrap loading plan.
5. Emit conflicts, missing evidence, and conservative fallbacks.
6. Validate JSON reports with `scripts/check.sh`.

## Output

- Environment detection summary.
- Evidence-tagged signal inventory.
- Capability profile and triad mode.
- Model tier and context budget decision.
- Bootstrap loading plan.
- Validation status and residual risks.
