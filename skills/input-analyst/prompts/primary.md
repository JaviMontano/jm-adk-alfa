---
name: input-analyst-primary
type: execution
version: 2.0.0
description: "Execute the Input Analyst workflow."
triad:
  lead: "input-analyst-lead"
  support: "input-analyst-support"
  guardian: "input-analyst-guardian"
---

# Input Analyst — Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|-----------|-------------|----------|-----------|
| `{{raw_input}}` | User message to analyze | Yes | User input |
| `{{context}}` | Background and constraints | No | User or codebase |
| `{{requested_passes}}` | Optional pass list | No | User or orchestrator |
| `{{routing_policy}}` | Offline/API permissions | Yes | Guardrails JSON |

## Execution Steps
1. Read SKILL.md `## When to Activate` — confirm this skill applies
2. If deterministic output is needed, create a JSON input matching `assets/input-analysis-schema.json`
3. Run `scripts/compile-input-analysis.py` with `routing_policy.offline_only=true` and `allow_external_apis=false`
4. If working manually, follow the five passes and preserve the same output sections as the script
5. Validate output against the Validation Gate before delivering

## Required Output Sections

- Surface errors
- 5 Whys
- 7 So-Whats
- Intent gap analysis
- Ambiguity register
- Actionability score
- Clarified prompt
- Routing hints
- User safety/privacy flags
- Confidence
