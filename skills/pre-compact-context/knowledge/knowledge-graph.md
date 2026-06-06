# Pre Compact Context - Knowledge Graph

## Core Concepts

- [[pre-compact-context]] - Primary context preservation skill.
- [[retention-map]] - P0/P1/P2/DROP classification table.
- [[p0-context]] - Verbatim context needed to avoid failure after compaction.
- [[compressed-summary]] - Meaning-preserving P1/P2 reduction.
- [[discard-list]] - Explicitly safe omissions with reasons.
- [[rehydration-prompt]] - Prompt that lets the next session resume.
- [[compaction-risk]] - Loss mode that can break continuity.

## Relationships

- [[pre-compact-context]] produces [[retention-map]].
- [[retention-map]] separates [[p0-context]], [[compressed-summary]], and
  [[discard-list]].
- [[rehydration-prompt]] depends on [[p0-context]] and unresolved
  [[compaction-risk]].
- [[discard-list]] must not contain [[p0-context]].

## Tags

#pre-compact-context #context-window #rehydration #jm-adk

## Cross-References

- `skills/session-end-cleanup` for final closeout after work completes.
- `skills/session-start-bootstrap` for resuming from a rehydration prompt.
- `skills/context-window-management` for ongoing context-budget monitoring.
- `skills/context-optimization` for compression tactics.
