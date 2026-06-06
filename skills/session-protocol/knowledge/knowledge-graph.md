# Session Protocol - Knowledge Graph

## Core Concepts

- [[session-protocol]] - Mandatory continuity workflow.
- [[context-loading]] - Ordered source reading.
- [[state-recovery]] - Recent changes, tasks, git, and spec state.
- [[pending-closure]] - Recommendations for open items.
- [[confirmation-gate]] - User approval before closure or execution.
- [[next-steps-proposal]] - Ranked action options.

## Relationships

- [[session-protocol]] starts with [[context-loading]].
- [[state-recovery]] depends on [[context-loading]].
- [[pending-closure]] depends on [[state-recovery]].
- [[confirmation-gate]] blocks task closure and implementation.
- [[next-steps-proposal]] follows [[pending-closure]].

## Tags

#session-protocol #state-recovery #confirmation-gate #jm-adk
