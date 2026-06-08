---
name: validate-hooks-primary
type: execution
version: 3.0.0
description: "Execute the offline Validate Hooks audit workflow."
triad:
  lead: "validate-hooks-lead"
  support: "validate-hooks-support"
  guardian: "validate-hooks-guardian"
---

# Validate Hooks Execute

## Inputs

| Parameter | Description | Required |
|---|---|---|
| `plugin_root` | Repository or plugin root that owns `hooks/hooks.json` | Yes |
| `hooks_json` | Parsed or referenced hooks configuration | Yes |
| `constraints` | Ownership, non-mutation, and reporting constraints | No |

## Execution Steps

1. [CODE] Read `SKILL.md`, `references/hook-compatibility-matrix.md`, and `assets/manifest.json`.
2. [CODE] If a local file audit is requested, read `hooks/hooks.json` only; do not execute hook commands.
3. [CODE] Run or mirror `scripts/compile-validate-hooks.py` to check structure, event names, hook type compatibility, ToolUseContext availability, command safety, and placement guard expectations.
4. [CODE] Render output with `templates/output.md` or `templates/output.html`.
5. [CODE] Report critical findings first, then warnings, remediation checklist, validation, and residual limits.

## Validation Gate

- [CODE] Findings include severity, event, hook type, rule, explanation, and remediation.
- [CODE] `prompt` and `agent` incompatibilities explicitly mention missing ToolUseContext.
- [CODE] Command hooks are inspected without execution.
- [CODE] Placement guard is checked as a PreToolUse command expectation.
- [CODE] Residual limits say offline checks cannot prove runtime command behavior.
