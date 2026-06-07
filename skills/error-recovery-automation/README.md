# Error Recovery Automation

Deterministic recovery planning for failed automations, scripts, CI jobs, API
calls, deployments, and agent workflows.

## Triggers

- `error-recovery-automation`
- `error recovery automation`
- `classify this failure`
- `retry safely`
- `rollback before retry`
- `escalate this failed automation`

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when a failed process needs a safe next step. The skill separates
recoverable transient failures from non-retryable failures, then produces a
bounded recovery plan with validation and handoff evidence.

## Output Format

Markdown or JSON with:

- failure summary
- classification and recoverability
- retry policy or retry block
- rollback plan when state can change
- escalation handoff when human action is required
- validation evidence
- residual risks and Guardian decision

Structured JSON plans can be validated offline with
`scripts/validate_error_recovery.py`.
