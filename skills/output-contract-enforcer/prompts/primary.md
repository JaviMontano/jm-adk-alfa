---
name: output-contract-enforcer-primary
type: execution
version: 2.0.0
description: "Execute the Output Contract Enforcer workflow."
triad:
  lead: "output-contract-enforcer-lead"
  support: "output-contract-enforcer-support"
  guardian: "output-contract-enforcer-guardian"
---

# Output Contract Enforcer - Execute

## Inputs

| Parameter | Description | Required |
|---|---|---|
| `{{contract}}` | Declared output contract, schema, or required section list | Yes |
| `{{artifact}}` | Generated output path or pasted output | Yes |
| `{{output_type}}` | markdown, json, html, docx-report, or unknown | Yes |
| `{{evidence_policy}}` | Whether evidence tags are mandatory | Yes |
| `{{naming_policy}}` | File naming rule when a path is present | No |

## Execution Steps

1. Confirm activation using `SKILL.md` `## When to Activate`.
2. Load `assets/contract-rules.json` and `assets/evidence-tag-policy.json`.
3. Load the contract and artifact.
4. Run deterministic checks in the documented order.
5. Return pass only when every mandatory check passes.
6. If a local file validation is requested, run `scripts/validate_output_contract.py`.

## Boundaries

- Do not design new schemas unless validation requires a repair suggestion.
- Do not auto-rename files.
- Do not skip evidence tags in quick mode.
