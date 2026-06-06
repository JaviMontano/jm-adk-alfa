# Example Output

## Session Summary

- [CONFIG] Active skill: `session-end-cleanup`.
- [CODE] Branch: `codex/harden-session-end-cleanup-dod-20260606`.
- [CODE] Scope was limited to `skills/session-end-cleanup/**`,
  `docs/audits/skills/session-end-cleanup-review.md`, and the ledger row for
  `session-end-cleanup`.

## Changes Completed

- [CODE] Added deterministic assets for activation, evidence, output contract,
  closure checklist, and durable update boundaries.
- [CODE] Added offline script validation with valid and negative fixtures.
- [CODE] Replaced scaffold examples and evals with session-closeout scenarios.

## Decisions And Assumptions

- [CONFIG] Durable ledger completion is allowed only after local validation
  passes.
- [ASSUMPTION] Remote CI has not been evaluated until a PR exists.

## Open Tasks

| ID | Status | Owner | Evidence | Next Action |
|---|---|---|---|---|
| SEC-001 | open | maintainer | [CONFIG] PR not opened | Open PR after local validation |

## Insights Captured

- [INFERENCE] A machine-checkable closeout report reduces false completion
  claims during multi-session work.

## Risks And Blockers

- [CODE] CI status is unavailable before PR creation.

## Validation Evidence

| Command | Status | Evidence |
|---|---|---|
| `bash skills/session-end-cleanup/scripts/check.sh` | pass | [CODE] Fixture validator accepted valid reports and rejected invalid reports |

## Durable Updates

- [CODE] Review doc updated after local validation.
- [CODE] Ledger row updated only for `session-end-cleanup`.

## Next Handoff

- [CONFIG] Open the PR, wait for CI, squash merge only if green, then update
  `main`.

## Guardian Decision

- [CONFIG] Block final completion until PR, CI, merge, and branch cleanup
  evidence exists.
