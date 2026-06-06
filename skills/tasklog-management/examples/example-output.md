# Example Output

## Tasklog Snapshot

- Path: `tasklog.md` [CODE]
- Status: `present` [CODE]
- Tasks reviewed: 2 [CODE]
- `as_of_date`: `2026-06-06` [CONFIG]

## Stale Review

| ID | Status | Last Update | Age Days | Decision | Evidence |
|---|---|---|---:|---|---|
| TL-015 | open | 2026-05-01 | 36 | `review_required` | [CODE] |
| TL-016 | completed | 2026-06-01 | 5 | `not_stale` | [CODE] |

## Bridge Review

| ID | Needs Bridge | Proposed Path | Action | Evidence |
|---|---:|---|---|---|
| TL-015 | true | `workspace/tasks/TL-015-export-validator/README.md` | create only if authorized | [INFERENCE] |

## Archive Review

| ID | Completed Date | Age Days | Decision | Evidence |
|---|---|---:|---|---|
| TL-016 | 2026-06-01 | 5 | retain | [CODE] |

## Guardian Decision

Decision: `block` [CONFIG]

Rationale: TL-015 is stale and needs owner review before any close, defer, or
bridge creation write. [CODE]
