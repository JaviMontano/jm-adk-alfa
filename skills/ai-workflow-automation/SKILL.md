---
name: ai-workflow-automation
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  LLM-in-the-loop workflows, human-AI handoff, approval gates. [EXPLICIT]
  Trigger: "ai workflow automation"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# AI Workflow Automation
> "Method over hacks."
## TL;DR
LLM-in-the-loop workflows, human-AI handoff, approval gates. [EXPLICIT]

Use this skill to design deterministic workflow plans where AI steps, human
approval gates, handoff artifacts, retries, fallbacks, and validation evidence
are explicit before execution. [EXPLICIT]

## Procedure
### Step 1: Discover
- Identify workflow goal, trigger, actors, inputs, outputs, risk level, and
  approval boundaries.
- Capture existing constraints, required human decisions, and source artifacts.
### Step 2: Analyze
- Classify actors with `assets/actor-taxonomy.json`.
- Model steps with `assets/workflow-schema.json`.
- Map approvals with `assets/approval-gate-policy.json`.
- Define handoffs with `assets/handoff-policy.json`.
- Define retries/fallbacks with `assets/failure-policy.json`.
### Step 3: Execute
- Produce a bounded workflow automation plan using `assets/report-contract.json`.
- Include AI prompt contracts, output contracts, human approval criteria, handoff
  packets, fallback paths, and deterministic validation checks.
### Step 4: Validate
- Verify quality criteria met
- For JSON plans, run `bash skills/ai-workflow-automation/scripts/check.sh`.

## Deterministic Assets

- `assets/manifest.json` lists local assets and consumers.
- `assets/workflow-schema.json` defines required workflow plan fields.
- `assets/actor-taxonomy.json` defines `human`, `ai`, and `system` actor rules.
- `assets/approval-gate-policy.json` defines gate criteria and decision values.
- `assets/handoff-policy.json` defines handoff packet requirements.
- `assets/failure-policy.json` defines bounded retry and fallback behavior.
- `assets/report-contract.json` defines the offline-validatable workflow plan.

## Quality Criteria
- [ ] Evidence tags applied
- [ ] Constitution-compliant
- [ ] Actionable output
- [ ] AI steps include prompt input contract and output contract
- [ ] High-risk or external-effect steps have approval gates before execution
- [ ] Human handoffs include artifact, owner, acceptance criteria, and evidence
- [ ] Retries are bounded and fallback paths are explicit
- [ ] Validation is reproducible without live network or current-time dependency

## Usage

Example invocations:

- "/ai-workflow-automation" — Run the full ai workflow automation workflow
- "ai workflow automation on this project" — Apply to current context
- "Design an LLM workflow with approval gates for support triage"
- "Create a human-AI handoff plan for invoice review automation"


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
| AI step lacks output contract | Block automation plan until contract exists |
| Approval owner missing | Mark as blocked; do not auto-approve |
| Retry policy says "until it works" | Replace with bounded retry limit and fallback |
