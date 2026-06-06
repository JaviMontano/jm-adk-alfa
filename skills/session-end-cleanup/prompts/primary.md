---
name: session-end-cleanup-primary
type: execution
version: 2.1.0
description: "Execute deterministic Session End Cleanup with triad validation."
triad:
  lead: "session-end-cleanup-lead"
  support: "session-end-cleanup-support"
  guardian: "session-end-cleanup-guardian"
---

# Session End Cleanup - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{objective}}` | User goal for the ending session | Yes | User input |
| `{{scope}}` | Active repo, workspace, branch, files, or task boundary | Yes | User input or local inspection |
| `{{evidence}}` | Commands, diffs, PR/CI/merge status, and artifacts inspected | Yes | Local inspection |
| `{{durable_update_authority}}` | Whether tasklog/changelog writes are authorized | No | User or repo policy |
| `{{output_format}}` | `markdown` or `json` | No | Default `markdown` |

## Execution

1. Read `skills/session-end-cleanup/assets/output-contract.json`.
2. Read `skills/session-end-cleanup/assets/evidence-policy.json`.
3. Inventory evidence before writing: git status, changed files, command output,
   PR/CI/merge state, blockers, and durable-log authority.
4. Lead produces the closeout sections in the fixed contract order.
5. Support checks for evidence gaps, false completion, hidden failures, and
   durable-log overreach.
6. Guardian approves only when required sections, evidence tags, validation
   outcomes, and next handoff are present.

## Output

Return the closeout packet with these sections:

- Session Summary
- Changes Completed
- Decisions And Assumptions
- Open Tasks
- Insights Captured
- Risks And Blockers
- Validation Evidence
- Durable Updates
- Next Handoff
- Guardian Decision
