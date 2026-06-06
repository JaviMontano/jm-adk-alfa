# Example Output

## Context Snapshot

- Feature: `billing-export` [CODE]
- Context path: `.specify/context.json` [CODE]
- Recorded stage: `specified` [CODE]

## Priming Sources

| Order | Source | Status | Evidence |
|---:|---|---|---|
| 1 | `.specify/context.json` | loaded | [CODE] |
| 2 | `.specify/plans/plan-20260606-billing-export.md` | loaded | [CODE] |
| 3 | `tasks.md` | missing | [OPEN] |
| 4 | `tests/features/billing-export.feature` | missing | [OPEN] |

## Stage Computation

Computed stage: `planned` [CODE]

Rationale: the plan artifact exists and the previous recorded stage was
`specified`, so the transition advances exactly one stage. [CODE]

## Persistence

- Target: `.specify/context.json`
- Action: update stage to `planned`
- Authorization: required before write [CONFIG]

## Next Action

Create or recover task evidence before moving to `tasks-ready`. [INFERENCE]

## Guardian Decision

Decision: `pass` for report quality; persistence remains approval-gated until
the workflow authorizes the context update. [CONFIG]
