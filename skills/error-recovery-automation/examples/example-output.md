# Example Output

## Failure Summary

- Workflow: nightly QA report publication. [EXPLICIT]
- Failed command: `python3 -B scripts/qa/run-adversarial-tests.py`. [EXPLICIT]
- Observed error: timeout while reading the QA fixture service. [EXPLICIT]
- State impact: no deployment, migration, or uploaded report artifact occurred. [EXPLICIT]

## Classification

- Category: `timeout`. [EXPLICIT]
- Recoverability: `retryable`. [EXPLICIT]
- Basis: the failure happened before external state changed and matches the
  transient timeout category in `assets/classification-policy.json`. [EXPLICIT]

## Recovery Plan

- Retry is allowed only after confirming the working tree is unchanged and the
  fixture service is reachable. [EXPLICIT]
- Retry command: `python3 -B scripts/qa/run-adversarial-tests.py`. [EXPLICIT]
- Bounds: maximum 3 attempts, exponential backoff, base delay 5 seconds, maximum
  delay 60 seconds, deterministic jitter disabled. [EXPLICIT]
- Stop conditions: repeated timeout after 3 attempts, a different error class,
  missing fixture evidence, or any state-changing side effect. [EXPLICIT]

## Rollback

- Rollback is not required because no deployment, migration, or report artifact
  was produced. [EXPLICIT]
- If a later retry creates a partial report artifact, delete only that artifact
  through the documented report cleanup command and rerun validation. [EXPLICIT]

## Escalation

- Escalate to the QA owner if the timeout repeats after the bounded retry window
  or if the error class changes. [EXPLICIT]
- Handoff must include the failed command, exit code, error excerpt, retry
  attempts, and validation output. [EXPLICIT]

## Validation Evidence

- Pre-retry: confirm clean worktree and fixture availability. [EXPLICIT]
- Post-recovery: rerun the adversarial test command and verify the report
  artifact exists with the expected checksum or manifest entry. [EXPLICIT]

## Guardian Decision

- Status: pass to retry within the stated bounds. [EXPLICIT]
- Remaining risk: external fixture availability may still fail and require owner
  escalation. [EXPLICIT]
