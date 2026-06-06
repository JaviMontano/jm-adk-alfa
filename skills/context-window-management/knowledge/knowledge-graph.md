# Context Window Management — Knowledge Graph

## Core Concepts

- token budget: maximum context, response reserve, available tokens, and final fit.
- priority policy: P0/P1/P2/P3 retention tiers.
- compression policy: allowed methods and preserved durable facts.
- eviction policy: P3-first eviction and P0 protection.
- budget report: machine-checkable keep/compress/evict plan.

## Cross-References

- `pre-compact-context` can use the budget report before compaction.
- `context-optimization` can tune retrieval and context selection after budget
  boundaries are set.
- `session-protocol` depends on P0 session state being preserved.
