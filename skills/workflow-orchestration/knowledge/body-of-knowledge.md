# Workflow Orchestration Body of Knowledge

## Domain

`workflow-orchestration` coordinates execution across multiple stages while preserving enough state to stop, resume, retry, or escalate without losing the thread.

## Required Anatomy

Every orchestration plan needs:

- Objective and trigger.
- Named agents.
- Inputs and outputs.
- Three to eight stages.
- Each stage with actions, outputs, checkpoint, resume state, failure signals, and recovery actions.
- Resume contract: token, state store, idempotency key, retry policy, and resume stage.
- Observability: logs, metrics, and audit trail.
- Completion criteria that define when the workflow is actually done.

## Failure Modes

| Failure | Why it breaks orchestration | Required response |
|---|---|---|
| No checkpoint | Phase transitions become subjective | Add criteria, evidence, pass action, and fail action |
| No resume token | A paused workflow cannot restart safely | Add token and state store |
| No idempotency key | Retries can duplicate work | Add key tied to input artifact or request id |
| Vague actions | Agents cannot reproduce the plan | Replace with observable actions |
| No observability | Completion cannot be audited | Add logs, metrics, and audit trail |
