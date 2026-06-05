---
name: workflow-orchestration
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Multi-step workflow execution with checkpoint and resume capability. [EXPLICIT]
  Trigger: "workflow orchestration"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Workflow Orchestration
> "Method over hacks."
## TL;DR
Multi-step workflow execution with checkpoint and resume capability. [EXPLICIT]

For deterministic output, prefer the bundled compiler:

```bash
python3 skills/workflow-orchestration/scripts/compile-orchestration-plan.py --input orchestration.json --output orchestration.md
```

Use `assets/orchestration-schema.json`, `assets/checkpoint-policy.json`, `assets/resume-policy.json`, and `assets/orchestration-template.md` as the contract before writing an orchestration plan by hand. [EXPLICIT]

## Procedure
### Step 1: Discover
- Gather context and requirements
### Step 2: Analyze
- Evaluate options per Constitution XIII/XIV
### Step 3: Execute
- Implement with evidence tags
### Step 4: Validate
- Verify quality criteria met

### Step 5: Persist Resume State
- Record resume token, state store, idempotency key, retry policy, and resume stage. [EXPLICIT]
- Do not mark complete unless checkpoints, observability, and completion criteria are recorded. [EXPLICIT]

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] `assets/manifest.json` lists schema, policies, and template used by `scripts/compile-orchestration-plan.py`
- [ ] `scripts/check.sh` passes with normal, incident-recovery, and invalid-resume fixtures
- [ ] Each stage has agent, inputs, actions, outputs, checkpoint, resumeState, failureSignals, and recoveryActions
- [ ] Resume contract names token, stateStore, idempotencyKey, retryPolicy, and resumeFrom
- [ ] Observability includes logs, metrics, and auditTrail

## Usage

Example invocations:

- "/workflow-orchestration" — Run the full workflow orchestration workflow
- "workflow orchestration on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |

## Deterministic Gate

Run `bash skills/workflow-orchestration/scripts/check.sh` when structured orchestration data is available or before shipping a reusable plan. The check validates JSON assets, positive fixtures, negative fixtures, Python syntax, and report fragments. [EXPLICIT]
