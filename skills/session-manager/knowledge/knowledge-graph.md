# Session Manager — Knowledge Graph

## Core Concepts

- `.specify/context.json`: persisted project state source.
- priming sources: context, latest plan, active tasks, and feature tests.
- stage policy: linear stage order and artifact evidence mapping.
- persistence policy: allowed `.specify/**` writes and authorization.
- Guardian block: required when evidence is missing, conflicting, or unsafe.

## Dependencies

- Upstream: session-start-bootstrap and session-protocol can invoke this skill to
  recover project state.
- Downstream: tasklog-management and changelog-management can use the status
  report as input after user confirmation.

## Validation

`scripts/validate_session_manager_report.py` validates the machine report
without network, time, or random dependencies.
