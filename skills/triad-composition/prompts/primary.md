---
name: triad-composition-primary
type: execution
version: 2.0.0
description: "Execute deterministic triad composition."
triad:
  lead: "triad-composition-lead"
  support: "triad-composition-support"
  guardian: "triad-composition-guardian"
---

# Triad Composition Primary Prompt

## Required Inputs

| Parameter | Description | Required |
|---|---|---|
| `[goal]` | What the user wants to accomplish | Yes |
| `[context]` | Project, domain, runtime, or artifact context | Yes |
| `[constraints]` | Safety, brand, quality, runtime, or deadline constraints | Yes |
| `[definition_of_done]` | How success will be judged | Yes |
| `[confidence]` | Match confidence, if already known | No |

## Execution

1. Load `SKILL.md`, `assets/composition-matrix.json`, and `assets/classification-policy.json`.
2. Confirm all required inputs or stop with `[OPEN]` clarification.
3. Classify domain using stable matching and tie-breakers.
4. Apply confidence-band action exactly.
5. Return a packet matching `assets/triad-output-contract.json`.
6. Guardian validates G0-G3 before delivery.

Never apply defaults for missing required inputs. Never skip Guardian in triad or committee mode.
