---
name: prompt-forge-primary
type: execution
version: 2.0.0
description: "Execute the Prompt Forge workflow."
triad:
  lead: "prompt-forge-lead"
  support: "prompt-forge-support"
  guardian: "prompt-forge-guardian"
---

# Prompt Forge - Execute

## Inputs

| Parameter | Description | Required |
|---|---|---|
| `{{mode}}` | create, review, evolve, repair, or port | Yes |
| `{{goal}}` | User outcome or prompt failure | Yes |
| `{{target_platform}}` | claude-project, custom-gpt, gemini-gem, api, or unknown | Yes |
| `{{source_boundary}}` | Allowed facts and unsupported behavior | Yes |
| `{{output_contract}}` | Required format or schema | Yes |

## Execution Steps

1. Confirm activation using `SKILL.md` `## When to Activate`.
2. Load assets listed in `SKILL.md` `## Assets And Scripts`.
3. Select mode and capture only missing contract-critical inputs.
4. Produce Playbook, scorecard, repair, or port packet.
5. Include happy path, edge case, and adversarial tests.
6. Validate against `SKILL.md` `## Validation Gate`.
7. When a JSON forge packet is produced, run `scripts/validate_forge_packet.py`.

## Boundaries

- Do not invent sources, platform limits, or domain policies.
- Do not expose hidden reasoning.
- Route durable prompt-file creation to `prompt-creator` after analysis approval.
