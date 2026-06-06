# Session End Cleanup - Knowledge Graph

## Core Concepts

- [[session-closeout]] - Evidence-backed final record of an agent session.
- [[validation-evidence]] - Commands, CI, PR, merge, or file evidence that proves
  the stated status.
- [[durable-update-boundary]] - Rule that tasklog/changelog writes must be
  authorized and scoped.
- [[false-completion]] - Risk of marking work done without proof.
- [[next-handoff]] - First concrete action for the next session.
- [[guardian-decision]] - Pass/block outcome with rationale.

## Relationships

- [[session-closeout]] requires [[validation-evidence]].
- [[durable-update-boundary]] prevents [[false-completion]] from becoming
  persistent state.
- [[guardian-decision]] blocks when [[validation-evidence]] is missing.
- [[next-handoff]] depends on unresolved tasks, risks, and blockers.

## Tags

#session-end-cleanup #handoff #validation-evidence #jm-adk

## Cross-References

- `skills/pre-compact-context` for context preservation before compaction.
- `skills/session-start-bootstrap` for resuming from a prior handoff.
- `skills/tasklog-management` for durable task state updates.
- `skills/changelog-management` for durable change history updates.
