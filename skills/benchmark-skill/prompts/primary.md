---
name: benchmark-skill-primary
type: execution
version: 2.1.0
description: "Execute a deterministic skill benchmark."
triad:
  lead: "benchmark-skill-lead"
  support: "benchmark-skill-support"
  guardian: "benchmark-skill-guardian"
---

# Benchmark Skill Primary Prompt

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---:|---|
| `{{state_a}}` | Baseline skill path or `[OPEN]` | Yes | User input |
| `{{state_b}}` | Candidate skill path or standard mode | Yes | User input |
| `{{mode}}` | version, against-standard, transformed, or different-skills | Yes | User input and validation |

## Execution Steps

1. Confirm the request is a skill benchmark using `## When To Activate`.
2. Verify each real state has `SKILL.md`; block if missing.
3. Load `assets/benchmark-rubric.json`, `assets/gate-policy.json`,
   `assets/net-assessment-policy.json`, and `assets/report-contract.json`.
4. Load `references/comparison-framework.md` for scoring calibration.
5. Inventory both states, score 10 dimensions, and run 13 gates.
6. Calculate deltas and classify net assessment exactly by policy.
7. Return an evidence-tagged report with regressions, trade-offs,
   improvements, recommendation, and caveats.
