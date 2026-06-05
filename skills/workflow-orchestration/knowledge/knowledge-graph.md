# Workflow Orchestration Knowledge Graph

- workflow-orchestration -> coordinates -> stage
- stage -> blocked_by -> checkpoint
- checkpoint -> records -> resume-token
- resume-token -> pairs_with -> idempotency-key
- stage -> detects -> failure-signal
- failure-signal -> triggers -> recovery-action
- workflow-orchestration -> requires -> observability
