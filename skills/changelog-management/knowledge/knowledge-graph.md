# Changelog Management — Knowledge Graph

## Core Concepts

- `changelog.md`: durable continuity source.
- entry contract: date, type, description, rationale, principles, evidence refs.
- entry type policy: decision, completion, amendment, insight, blocker, discovery.
- ordering policy: explicit-date, newest-first sections.
- dedupe policy: fingerprint before append.
- evidence policy: rationale, principle, and evidence reference requirements.

## Cross-References

- `session-protocol` reads recent changelog entries during state recovery.
- `session-end-cleanup` can propose changelog entries during handoff.
- `tasklog-management` tracks open work separately from continuity entries.
