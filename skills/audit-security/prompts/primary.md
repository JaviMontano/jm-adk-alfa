---
name: audit-security-primary
type: execution
version: 2.0.1
description: "Execute the deterministic Audit Security workflow."
triad:
  lead: "audit-security-lead"
  support: "audit-security-support"
  guardian: "audit-security-guardian"
---

# Audit Security Execute

## Dynamic Parameters

| Parameter | Description | Required |
|---|---|---|
| `{{target}}` | Plugin root or explicit file list | Yes |
| `{{scope}}` | Optional scan boundaries or exclusions | No |
| `{{format}}` | Markdown or JSON report | No |

## Execution Steps

1. Confirm activation with `assets/activation-policy.json`.
2. Load `assets/scan-policy.json`, `assets/evidence-policy.json`, and `assets/report-contract.json`.
3. Execute all six static scan categories.
4. Produce stable `SEC-NNN` findings with path, line, pattern, evidence, and remediation.
5. Add false-positive notes for placeholders and documentation examples.
6. Add remediation plan entries for all CRITICAL and WARNING findings.
7. Validate JSON reports with the local validator when available.
