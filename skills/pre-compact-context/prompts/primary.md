---
name: pre-compact-context-primary
type: execution
version: 2.1.0
description: "Execute deterministic Pre Compact Context with triad validation."
triad:
  lead: "pre-compact-context-lead"
  support: "pre-compact-context-support"
  guardian: "pre-compact-context-guardian"
---

# Pre Compact Context - Execute

## Dynamic Parameters

| Parameter | Description | Required | Filled By |
|---|---|---|---|
| `{{objective}}` | Active goal to preserve | Yes | User input |
| `{{scope}}` | Repo, branch, files, PR, or task boundary | Yes | Local inspection |
| `{{context_sources}}` | Files, commands, docs, and state read before compaction | Yes | Local inspection |
| `{{token_pressure}}` | low / medium / high / critical | No | User or runtime |
| `{{output_format}}` | `markdown` or `json` | No | Default `markdown` |

## Execution

1. Read `assets/retention-policy.json` and `assets/output-contract.json`.
2. Inventory current objective, hard rules, git state, changed files, command
   evidence, PR/CI state, decisions, assumptions, blockers, and next action.
3. Classify each item as P0, P1, P2, or DROP.
4. Lead produces the fixed packet sections.
5. Support checks for context loss, false compression, and secret exposure.
6. Guardian approves only when P0 items and rehydration prompt are complete.

## Output

Return:

- Compaction Trigger
- Preserve Verbatim
- Compressed Summary
- Discard List
- Open Questions
- Risks And Blockers
- Validation Evidence
- Rehydration Prompt
- Guardian Decision
