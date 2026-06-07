---
name: error-recovery-automation
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Designs deterministic recovery plans for failed automations: error
  classification, bounded retry, rollback, escalation, validation, and
  evidence handoff. [EXPLICIT]
  Trigger: "error recovery automation"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Error Recovery Automation

> "Method over hacks."

## TL;DR

Use this skill when an automation, CI job, agent workflow, script, API call, or
deployment failed and the next action must be safe, repeatable, and auditable.
[EXPLICIT]

The output is a recovery plan, not a blind rerun. It must classify the failure,
decide whether retry is allowed, define bounded backoff, require rollback when
state can be corrupted, and provide validation evidence before marking recovery
complete. [EXPLICIT]

## Procedure

### Step 1: Capture Failure Evidence

- Record the failed command or workflow, exit code or error class, scope,
  affected state, last safe checkpoint, and available logs.
- Do not invent logs, timestamps, service status, or root cause.

### Step 2: Classify Recoverability

- Use `assets/classification-policy.json` to classify the error as retryable,
  non-retryable, human-required, or blocked by missing evidence.
- Treat authentication, authorization, schema, data corruption, missing config,
  destructive side effects, and unknown state as non-retryable until evidence
  proves otherwise.

### Step 3: Design The Recovery Plan

- If retry is allowed, use `assets/retry-policy.json` for bounded attempts,
  deterministic backoff, idempotency checks, and stop conditions.
- If state may have changed, use `assets/rollback-policy.json` before any retry.
- If the issue requires an owner decision, use `assets/escalation-policy.json`
  and prepare a handoff with evidence.

### Step 4: Validate And Handoff

- Produce the required sections from `assets/error-recovery-contract.json`.
- Validate structured JSON recovery plans with
  `scripts/validate_error_recovery.py` or `scripts/check.sh` when an offline
  gate is needed.
- Mark recovery complete only when post-recovery checks pass and evidence is
  attached.

## Quality Criteria

- [ ] Failure evidence is explicit and traceable.
- [ ] Error category and recoverability are justified.
- [ ] Retry is bounded, deterministic, idempotent, and stopped on policy breach.
- [ ] Rollback is defined when state, data, deployment, or config may change.
- [ ] Escalation is explicit when retry is unsafe or evidence is insufficient.
- [ ] Validation commands, expected outcomes, and residual risks are recorded.
- [ ] Evidence tags are applied to user-facing factual claims.

## Usage

Example invocations:

- "/error-recovery-automation" - Build a recovery plan for a failed workflow.
- "Classify this CI failure and decide if retry is safe."
- "Create a rollback and escalation plan before rerunning this deployment."
- "Validate this recovery JSON against the deterministic contract."

## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not execute destructive remediation without explicit approval [EXPLICIT]
- Does not replace domain owner judgment for production incidents [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Produce an evidence gap report and request the minimum failure evidence |
| Conflicting retry and safety requirements | Block retry, preserve state, and escalate |
| Unknown state after partial execution | Require rollback or checkpoint validation before recovery |
| Rate limits or transient network failures | Allow bounded retry only with idempotency and stop conditions |
| Authentication, schema, or configuration failures | Do not retry blindly; escalate or fix root cause first |
| Destructive action requested | Require approval, rollback plan, and post-action validation |
