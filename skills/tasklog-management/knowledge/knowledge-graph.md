# Tasklog Management — Knowledge Graph

## Core Concepts

- `tasklog.md`: cross-session source of task truth.
- task schema: ID, description, status, owner, opened date, last-update date,
  bridge, and notes.
- status policy: allowed lifecycle transitions.
- staleness policy: explicit-date stale and archive calculations.
- bridge policy: deterministic `workspace/tasks/TL-NNN-<slug>/README.md` paths.
- Guardian block: required for invalid IDs, stale omissions, and unauthorized writes.

## Cross-References

- `session-protocol` reads tasklog state during session initialization.
- `session-end-cleanup` can propose tasklog updates during handoff.
- `changelog-management` records broader project decisions outside task rows.
