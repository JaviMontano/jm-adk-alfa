---
name: google-workspace-apis-primary
type: execution
version: 2.1.0
description: "Execute a deterministic Google Workspace API integration plan."
triad:
  lead: "google-workspace-apis-lead"
  support: "google-workspace-apis-support"
  guardian: "google-workspace-apis-guardian"
---

# Google Workspace APIs — Execute

## Inputs

| Parameter | Description | Required |
|---|---|---|
| `{{task}}` | Business workflow to automate | Yes |
| `{{services}}` | Gmail, Calendar, Drive, Docs, Sheets, Slides | Yes |
| `{{runtime}}` | REST/client library, MCP, or mixed | Yes |
| `{{constraints}}` | Security, privacy, quota, compliance limits | No |

## Workflow

1. Read `knowledge/body-of-knowledge.md`.
2. Read the deterministic assets under `assets/`.
3. Normalize the request into the compiler schema.
4. Use the narrowest OAuth scope profile per operation.
5. Enforce read-only-first before every mutation.
6. Map MCP tools only when the tool belongs to the service/action.
7. Run or instruct the user to run `scripts/compile-google-workspace-apis.py`.
8. Report validation, limits, and live-check prerequisites.

## Required Output

- Summary with evidence tags.
- Service matrix with exact method names.
- OAuth scope plan and secrets policy.
- MCP tool mapping when relevant.
- Retry, idempotency, rollback, and validation matrix.
- Explicit statement that offline checks do not prove live Google access.
