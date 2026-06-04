---
name: x-ray-skill-primary
type: execution
version: 2.0.0
description: "Execute the X-Ray skill-quality diagnostic workflow."
triad:
  lead: "x-ray-skill-lead"
  support: "x-ray-skill-support"
  guardian: "x-ray-skill-guardian"
---

# X-Ray Skill -- Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{skill_path}}` | Path to the skill directory to audit | Yes | User input |
| `{{depth}}` | quick / standard / deep | No | User or auto |
| `{{output_format}}` | markdown / json | No | User or auto |

## Execution Steps

1. Confirm `{{skill_path}}` contains top-level `SKILL.md`.
2. Load `references/gold-standard-anatomy.md` and `references/quality-rubric.md`.
3. Run `scripts/compile-x-ray-report.py` when deterministic scoring is appropriate.
4. Read any files the compiler flags as weak or unresolved.
5. Return the X-Ray report with scores, gates, issues, components, and next step.
