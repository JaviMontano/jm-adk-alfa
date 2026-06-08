---
name: google-apis-integration-primary
type: execution
version: 2.0.0
description: "Execute the offline Google APIs integration planning workflow."
triad:
  lead: "google-apis-integration-lead"
  support: "google-apis-integration-support"
  guardian: "google-apis-integration-guardian"
---

# Google APIs Integration - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{task}}` | Integration objective and target Google services | Yes | User input |
| `{{context}}` | App architecture, runtime, data classes, and constraints | Yes | User or codebase |
| `{{constraints}}` | Security, consent, quota, deployment, or compliance rules | No | Guardrails |
| `{{fixture}}` | Structured JSON input for deterministic compiler | No | User or generated draft |

## Execution Steps

1. Read `SKILL.md`, `assets/manifest.json`, and `assets/source-map.md`. [CODE]
2. Convert the request into the stable schema in `assets/google-apis-integration-schema.json`. [CODE]
3. Run `scripts/compile-google-apis-integration.py` when the request has enough structured data. [CODE]
4. If data is missing, return a gap checklist using `templates/output.md` sections. [CODE]
5. Validate consent, scopes, secrets, retry/idempotency, service operations, and test matrix before delivery. [CODE]
