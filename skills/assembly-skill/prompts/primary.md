---
name: assembly-skill-primary
type: execution
version: 2.1.0
description: "Execute one deterministic Assembly Skill workflow."
triad:
  lead: "assembly-skill-lead"
  support: "assembly-skill-support"
  guardian: "assembly-skill-guardian"
---

# Assembly Skill — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{target_skill}}` | Single skill directory path | Yes | User input |
| `{{mode}}` | quick, standard, deep, or auto | No | User or mode policy |
| `{{write_approval}}` | Gate B approval state | For writes | User |

## Execution Steps

1. Read `SKILL.md ## When to Activate`.
2. Read `assets/mode-policy.json`.
3. Refuse multiple target skills.
4. Run Phase A and select mode.
5. Stop before writes until Gate B is explicit.
6. Build the final report from `assets/assembly-report-template.md`.
7. Validate with `scripts/validate_assembly_contract.py`.
