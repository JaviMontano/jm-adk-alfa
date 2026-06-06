# Example Output

## Compaction Trigger

- [CONFIG] User requested context preservation before compaction.

## Preserve Verbatim

| Priority | Item | Source | Reason | Evidence |
|---|---|---|---|---|
| P0 | Exactly one skill, one branch, one PR, one green merge at a time. | User workflow | Active hard rule | [CONFIG] |
| P0 | Active skill is `pre-compact-context`. | User workflow | Prevents parallel skill work | [CONFIG] |
| P1 | Branch is `codex/harden-pre-compact-context-dod-20260606`. | Git state | Resume point | [CODE] |

## Compressed Summary

- [CODE] The skill was hardened with deterministic assets, evals, examples,
  prompts, templates, knowledge, and scripts.

## Discard List

- [INFERENCE] Repeated progress updates can be dropped because the packet keeps
  final state and validation commands.

## Open Questions

- [OPEN] PR URL is not available until the PR is created.

## Risks And Blockers

- [CONFIG] Do not merge until local validations and CI pass.

## Validation Evidence

| Command | Status | Evidence |
|---|---|---|
| `bash skills/pre-compact-context/scripts/check.sh` | pass | [CODE] Valid fixtures passed and negative fixtures failed |

## Rehydration Prompt

Continue `pre-compact-context` hardening in
`/Users/deonto/Documents/workspace/jm-adk-alfa`. Verify `git status --short
--branch`, rerun the required local validations, open the PR if clean, wait for
CI, squash merge only if green, update `main`, and do not start the next skill
until Guardian authorizes.

## Guardian Decision

- [CONFIG] Pass for compaction only if the packet remains available to the next
  session.
