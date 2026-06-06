---
name: ai-architecture-audit-primary
type: execution
version: 2.0.0
description: "Execute the AI Architecture Audit workflow."
triad:
  lead: "ai-architecture-audit-lead"
  support: "ai-architecture-audit-support"
  guardian: "ai-architecture-audit-guardian"
---

# AI Architecture Audit — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{system}}` | Existing AI system to audit | Yes | User input |
| `{{evidence}}` | Code, config, docs, metrics, interviews, tool outputs | Yes | Workspace/user |
| `{{scope}}` | structural / quality / security / debt / genai / full | No | User/default |
| `{{depth}}` | express / standard / deep | No | User/default |

## Execution Steps
1. Confirm the task audits an existing AI system.
2. Load `assets/` policies and relevant `references/`.
3. Inventory evidence and scope limitations before findings.
4. Evaluate D1-D6 and record all omissions with rationale.
5. Create findings with severity, evidence, and remediation.
6. Build roadmap and validation section.
7. Validate JSON packet with `scripts/check.sh` when present.
