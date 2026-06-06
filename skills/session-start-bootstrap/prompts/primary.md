---
name: session-start-bootstrap-primary
type: execution
version: 2.1.0
description: "Execute deterministic Session Start Bootstrap with triad validation."
triad:
  lead: "session-start-bootstrap-lead"
  support: "session-start-bootstrap-support"
  guardian: "session-start-bootstrap-guardian"
---

# Session Start Bootstrap - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{objective}}` | Current user goal | Yes | User input |
| `{{repo}}` | Active repo/workspace | Yes | User input or local inspection |
| `{{handoff}}` | Prior ReleasePacket or rehydration packet | No | User or local docs |
| `{{constraints}}` | Hard rules and pause criteria | Yes | User/repo instructions |
| `{{output_format}}` | `markdown` or `json` | No | Default `markdown` |

## Execution

1. Read `assets/environment-policy.json`, `assets/context-loading-policy.json`,
   and `assets/guardrails-policy.json`.
2. Verify repo, branch, dirty-tree state, open PR state, and baseline SHA when
   relevant.
3. Load only task-relevant context sources and list each one.
4. Record hard rules, blockers, validation baseline, and first safe action.
5. Support reviews for missing evidence and over-loading.
6. Guardian approves or blocks startup.

## Output

Return Environment, Context Sources Loaded, Active Guardrails, Current State,
Blockers And Gaps, Validation Baseline, First Action, and Guardian Decision.
