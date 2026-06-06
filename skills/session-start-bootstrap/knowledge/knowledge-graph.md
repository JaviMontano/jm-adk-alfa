# Session Start Bootstrap - Knowledge Graph

## Core Concepts

- [[session-start-bootstrap]] - Startup gate before agent work.
- [[environment-check]] - Repo, branch, dirty tree, and PR state proof.
- [[context-source-list]] - Minimal list of loaded sources.
- [[guardrails-initialization]] - Hard rules, forbidden changes, and pause criteria.
- [[source-precedence]] - Order for resolving conflicts.
- [[first-action]] - Concrete next step after startup.
- [[startup-blocker]] - Condition that prevents safe work.

## Relationships

- [[session-start-bootstrap]] requires [[environment-check]].
- [[context-source-list]] feeds [[guardrails-initialization]].
- [[source-precedence]] resolves conflicts in [[guardrails-initialization]].
- [[startup-blocker]] can block [[first-action]].

## Tags

#session-start-bootstrap #environment-check #guardrails #jm-adk

## Cross-References

- `skills/pre-compact-context` for rehydration packets.
- `skills/session-end-cleanup` for ReleasePackets.
- `skills/environment-detection` for deeper platform checks.
- `skills/session-manager` for lifecycle orchestration.
