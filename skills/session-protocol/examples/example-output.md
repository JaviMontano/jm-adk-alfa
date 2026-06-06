# Example Output

## Context Loading

| Order | Source | Status | Evidence |
|---|---|---|---|
| 1 | `CLAUDE.md` | loaded | [DOC] |
| 2 | `references/ontology/constitution-v6.0.0.md` | loaded | [DOC] |
| 3 | `insights/README.md` | missing | [OPEN] |

## State Recovery

- [CODE] Current branch is `main`.
- [DOC] Last changelog entries show one recently merged hardening PR.

## Pending Closure

| Item | Age | Recommendation | Evidence |
|---|---:|---|---|
| `TASK-014` | 9 days | continue | [DOC] Still aligns with active queue |

## Next Steps Proposal

1. [CONFIG] Continue the active hardening queue with the next skill.
2. [INFERENCE] Review stale tasks before adding new work.

## Confirmation Gate

- [CONFIG] No tasks will be closed or archived until the user confirms.

## Guardian Decision

- [CONFIG] Pass for initialization; wait for user direction before execution.
