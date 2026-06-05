# Quality Gatekeeper Output

## Summary

| Field | Value |
|---|---|
| Gate scope | `{G0|G1|G2|G3}` |
| Source stage | `{source_stage}` |
| Target stage | `{target_stage}` |
| Overall status | `{pass|blocked|not_verified}` |
| Blocking findings | `{count}` |
| Not verified | `{count}` |
| Assumption ratio | `{0.00-1.00}` |
| Confidence | `{0.00-1.00}` |

## Gate Results

| Gate | Status | Blocking | Evidence |
|---|---|---:|---|
| `{gate}` | `{status}` | `{true|false}` | `{tagged evidence}` |

## Criteria Results

| Gate | Criterion | Status | Severity | Evidence | Remediation |
|---|---|---|---|---|---|
| `{gate}` | `{criterion}` | `{status}` | `{severity}` | `{tagged evidence}` | `{remediation or none}` |

## Violations

| Criterion | Finding | Severity | Remediation |
|---|---|---|---|
| `{criterion}` | `{tagged finding}` | `{severity}` | `{action}` |

## Missing Evidence

| Criterion | Missing | Next Step |
|---|---|---|
| `{criterion}` | `{missing evidence}` | `{file, command, or decision}` |

## Remediation Plan

{ordered remediation plan}

## Proposed Score-History Entry

```json
{score_history_entry}
```

## Decision

- release_decision: `{allow|block|needs_evidence}`
- reason: `{tagged reason}`
- next_action: `{next command, file, or decision}`

## Caveats

{explicit caveats}
