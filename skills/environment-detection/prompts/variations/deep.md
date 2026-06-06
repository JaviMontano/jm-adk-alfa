---
name: environment-detection-deep
type: variation
version: 2.0.0
description: "Environment Detection — deep analysis mode. Exhaustive coverage."
---

# Environment Detection — Deep Mode

## When to Use

Use deep mode when environment signals conflict, bootstrap policy will affect many skills, or the user asks for a reusable runtime report.

## Dynamic Parameters

| Parameter | Required | Filled By |
|-----------|----------|-----------|
| `{{task}}` | Yes | User input |
| `{{signals}}` | Yes | Workspace, tools, model/context metadata |
| `{{depth}}` | No | Set to "deep" |

## Execution (Deep)

1. Inventory all local instruction markers and tool capabilities.
2. Score conflicts by source strength: explicit runtime > tool availability > repo file marker > user assumption.
3. Produce pass/warn/block status with exact conflict reasons.
4. Build JSON matching `assets/environment-report-contract.json`.
5. Run `scripts/check.sh` or the Python validator against the JSON.

## Output

- Full signal inventory.
- Deterministic mapping decisions.
- Conflict and degradation analysis.
- Tier-safe bootstrap plan.
- JSON validation evidence.
