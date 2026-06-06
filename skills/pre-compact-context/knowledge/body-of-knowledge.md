# Pre Compact Context - Body of Knowledge

## Purpose

Pre-compaction preservation protects continuity when the conversation is about
to be summarized, compressed, or resumed elsewhere. It is not a general recap:
it is a retention decision system.

## Retention Classes

| Priority | Meaning | Examples |
|---|---|---|
| P0 | Must preserve verbatim | Hard rules, active objective, branch/PR state, blockers, next action |
| P1 | Preserve precisely or summarize with exact references | File paths, commands, decisions, assumptions, validation evidence |
| P2 | Compress aggressively | Background, repeated rationale, non-current alternatives |
| DROP | Safe to omit | Duplicates, stale plans, disproven facts, social filler |

## Evidence Rules

- P0 items require source, reason, and evidence tag.
- P1 items require enough source detail for lookup.
- P2 items may be summarized but must not alter meaning.
- DROP items require a reason and must never contain active blockers, hard rules,
  validation failures, branch/PR state, or next action.

## Rehydration Prompt Requirements

The prompt for the next session must include:

- Active repo/workspace and branch.
- Active objective and current skill/task.
- First command or file to inspect.
- First decision to make or first blocker to resolve.
- Validation commands or PR/CI state when relevant.
- Explicit warning about any `[OPEN]` source gap.

## Anti-Patterns

- Compacting away the current blocker.
- Replacing exact file paths with vague area names.
- Dropping the user's hard rules to save space.
- Preserving secrets verbatim.
- Saying "all validations passed" without command evidence.
- Treating conflicting state as resolved.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---:|---|
| P0 source coverage | 100% | Every P0 item has source and evidence tag |
| Rehydration completeness | 100% | Prompt includes repo, branch, objective, first action |
| Unsafe DROP count | 0 | DROP contains no hard rules, blockers, validation failures |
| Secret echo count | 0 | Secrets are redacted |

## Failure Modes

- Unknown state: preserve as `[OPEN]` and include a verification command.
- Conflicting state: preserve both claims and block final compaction pass if the
  conflict changes next action.
- Token pressure: keep P0/P1 first, compress P2, then DROP duplicates.
