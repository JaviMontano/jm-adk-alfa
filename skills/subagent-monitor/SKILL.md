---
name: subagent-monitor
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Track subagent execution with deterministic timeout policy, typed results, partial failure aggregation, evidence, and offline validation. Trigger: "subagent monitor"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---
# Subagent Monitor
> "Method over hacks."
## TL;DR
Track subagent execution with deterministic timeout policy, typed results, partial failure aggregation, evidence, and offline validation.

## Deterministic Contract

Use `assets/subagent-monitor-report-contract.json` and validate reports with `scripts/validate_subagent_monitor_report.py`. A valid report must include:

- Stable `swarm_id` and task summary.
- Agent registry with deterministic roles and status values.
- Timeout policy that is bounded, monotonic, and not based on wall-clock evidence.
- One typed result per agent with `agent_id`, `status`, `result_type`, evidence tag, and optional error.
- Aggregation policy that preserves blockers and partial failures instead of reporting success silently.
- Evidence entries with approved tags and source.
- Validation checks for assets, deterministic scripts, quality criteria, timeout policy, typed results, aggregation policy, partial failure handling, and evidence.
## Procedure
### Step 1: Discover
- Gather agent list, task contract, timeout budget, and expected result types.
### Step 2: Analyze
- Identify timeout and partial-failure policy before dispatch.
### Step 3: Execute
- Track sequence-based start/completion, collect typed results, and record errors.
### Step 4: Validate
- Run the offline report validator before accepting the aggregate result.
## Quality Criteria
- [ ] Evidence tags applied
- [ ] Timeout policy is bounded and non-silent
- [ ] Every agent has exactly one typed result
- [ ] Aggregation status reflects blockers, warnings, and coverage gaps
- [ ] Offline validator passes

## Usage

Example invocations:

- "/subagent-monitor" — Run the full subagent monitor workflow
- "subagent monitor on this project" — Apply to current context


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
