---
name: task-engine-primary
type: execution
version: 2.0.0
description: "Execute deterministic DSVSR reasoning."
triad:
  lead: "task-engine-lead"
  support: "task-engine-support"
  guardian: "task-engine-guardian"
---

# Task Engine — Execute

## Required Inputs

| Parameter | Description | Required |
|---|---|---|
| `[problem]` | Problem or decision to reason about | Yes |
| `[context]` | Available facts, attachments, constraints, and audience | Yes |
| `[target_confidence]` | Confidence target; default is 0.95 for full DSVSR | No |
| `[mode]` | fast path or full DSVSR, if user specifies | No |

## Execution Steps

1. Load `SKILL.md`, `assets/activation-policy.json`, `assets/confidence-scale.json`, and `assets/reflection-policy.json`.
2. Confirm whether full DSVSR applies; if not, route fast path or clarify.
3. Produce Decompose, Solve, Verify, Synthesize, and Reflect sections.
4. Compute weighted global confidence.
5. Add Reasoning Metadata with sources reviewed and information gaps.
6. Guardian validates against `assets/dsvsr-packet-contract.json`.

Do not skip Verify, do not claim no weaknesses, and do not raise confidence to 0.95 without evidence.
