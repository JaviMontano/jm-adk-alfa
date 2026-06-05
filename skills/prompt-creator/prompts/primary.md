---
name: prompt-creator-primary
type: execution
version: 2.0.0
description: "Execute the Prompt Creator workflow."
triad:
  lead: "prompt-creator-lead"
  support: "prompt-creator-support"
  guardian: "prompt-creator-guardian"
---

# Prompt Creator - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{task}}` | What to accomplish | Yes | User input |
| `{{context}}` | Background and constraints | Yes | User or codebase |
| `{{constraints}}` | Additional rules | No | Guardrails JSON |

## Execution Steps
1. Read SKILL.md `## When to Activate` and confirm this skill applies.
2. Read `assets/prompt-type-matrix.json` and classify prompt type.
3. Read the source agent file or return a `missing_source_agent` gap packet.
4. Check existing prompt paths before selecting the target filename.
5. Generate the prompt artifact using the required sections for the type.
6. Apply `assets/prompt-contract-checklist.md`.
7. Validate with `scripts/validate_prompt_artifact.py` when an artifact is produced.
8. Return decision, artifact or gap, validation evidence, and next action.
