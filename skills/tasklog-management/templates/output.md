# Tasklog Management Report

## Tasklog Snapshot

- Path: `{tasklog_path}` `{evidence_tag}`
- Status: `{tasklog_status}` `{evidence_tag}`
- Tasks reviewed: `{task_count}` `{evidence_tag}`
- `as_of_date`: `{as_of_date}` `{evidence_tag}`

## Operations

| Operation | ID | From | To | Authorized | Evidence |
|---|---|---|---|---:|---|
| `{operation}` | `{task_id}` | `{from_status}` | `{to_status}` | `{authorized}` | `{evidence_tag}` |

## Stale Review

| ID | Status | Last Update | Age Days | Stale | Action | Evidence |
|---|---|---|---:|---:|---|---|
| `{task_id}` | `{status}` | `{last_update}` | `{age_days}` | `{stale}` | `{action}` | `{evidence_tag}` |

## Bridge Review

| ID | Needs Bridge | Bridge Path | Exists | Action | Evidence |
|---|---:|---|---:|---|---|
| `{task_id}` | `{needs_bridge}` | `{bridge_path}` | `{exists}` | `{action}` | `{evidence_tag}` |

## Archive Review

| ID | Completed Date | Age Days | Archive Eligible | Action | Evidence |
|---|---|---:|---:|---|---|
| `{task_id}` | `{completed_date}` | `{age_days}` | `{archive_eligible}` | `{action}` | `{evidence_tag}` |

## Guardian Decision

Decision: `{decision}` `{evidence_tag}`

Rationale: `{rationale}` `{evidence_tag}`
