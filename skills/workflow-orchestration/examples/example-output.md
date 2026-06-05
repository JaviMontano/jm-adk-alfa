<!--
generated-by: scripts/scaffold-skill.py
generated-for: workflow-orchestration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

# Product Launch Orchestration

## Objective

Coordinate launch readiness from brief intake through verified go/no-go decision.

## Stages

### 1. Intake planning (ready)
- Agent: product-manager
- Checkpoint: Scope checkpoint -> pass=continue fail=retry-with-input
- Resume state: stageKey=intake-planning, artifact=workspace/launch/checkpoint-log.md

### 2. Execution coordination (pending)
- Agent: release-coordinator
- Checkpoint: Readiness checkpoint -> pass=continue fail=escalate
- Resume state: stageKey=execution-coordination, artifact=workspace/launch/readiness-matrix.md

### 3. Verification review (pending)
- Agent: quality-gatekeeper
- Checkpoint: Go/no-go checkpoint -> pass=continue fail=stop
- Resume state: stageKey=verification-review, artifact=workspace/launch/decision.md

## Resume Contract

- Token: `launch-ready-001`
- State store: `checkpoint-file`
- Idempotency key: `launch-brief-sha256`
- Retry policy: `manual-review`
- Resume from stage: `1`
