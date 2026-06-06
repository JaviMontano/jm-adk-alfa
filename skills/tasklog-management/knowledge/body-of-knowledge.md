# Tasklog Management — Body of Knowledge

## Canon

`tasklog.md` is a compact cross-session task ledger. It captures durable work
items that need continuity across agent sessions. The ledger should stay small,
evidence-backed, and safe to scan during session start and session close.

## Task Lifecycle

| Status | Meaning | Allowed Next States |
|---|---|---|
| `open` | Work is known but not started. | `in-progress`, `blocked`, `deferred`, `completed` |
| `in-progress` | Work has started. | `blocked`, `deferred`, `completed` |
| `blocked` | Work is waiting on input or dependency. | `in-progress`, `deferred`, `completed` |
| `deferred` | Work is intentionally postponed. | `open`, `in-progress`, `completed` |
| `completed` | Work is done and retained for 30 days. | none |

## Deterministic Dates

Stale and archive calculations require explicit `as_of_date`. Active tasks older
than 14 days since `Last Update` require review. Completed tasks older than 30
days are archive-eligible, but archive writes remain authorization-gated.

## Bridge Contract

Use `workspace/tasks/TL-NNN-<slug>/README.md` when a task needs working files,
evidence bundles, or multi-session continuation. Bridge creation requires
authorization.

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| ID validity | 100% | Every ID matches `TL-NNN`. |
| Status validity | 100% | Every status is allowed and transition-valid. |
| Stale accuracy | 100% | `age_days` equals `as_of_date - Last Update`. |
| Bridge determinism | 100% | Required bridge paths match the policy pattern. |
| Offline validation | 100% | `bash skills/tasklog-management/scripts/check.sh` passes. |

## Anti-Patterns

- Closing stale tasks automatically.
- Computing stale age from hidden system time.
- Reusing or skipping task IDs without evidence.
- Creating bridge folders without authorization.
- Mixing changelog decisions into tasklog rows.
