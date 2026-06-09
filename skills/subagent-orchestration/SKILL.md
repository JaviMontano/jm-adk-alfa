---
name: subagent-orchestration
version: 1.1.0
description: "Design deterministic hub-and-spoke subagent orchestration plans with AgentDefinition plus Task dispatch, fresh-session context isolation, typed spoke errors, local recovery, coverage-gap aggregation, and bounded partial-failure behavior."
owner: "JM Labs"
triggers:
  - subagent orchestration
  - hub and spoke
  - coordinator agents
  - error propagation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Subagent Orchestration

## Purpose

Design deterministic hub-and-spoke coordinators that dispatch isolated subagents through `AgentDefinition` plus `Task`, then aggregate typed spoke results without hiding partial failures. The skill is for architecture plans, code skeletons, and review packets where context isolation, model/tool assignment, and error propagation must be verifiable.

## Deterministic Contract

Use `assets/orchestration-contract.json` and validate JSON plans with `scripts/validate_orchestration_plan.py`. A valid plan must include:

- A coordinator that consumes only the final spoke message.
- Two or more spoke definitions with `AgentDefinition` fields, minimal tools, model role, and `Task` dispatch.
- Fresh-session context isolation for every spoke.
- Typed spoke failures with `failure_type`, `attempted_query`, `partial_results`, and `suggested_alternatives`.
- Local recovery before propagation.
- Aggregation that continues on partial failure and records explicit coverage gaps.
- Validation flags: `offline=true`, `network_required=false`, `deterministic=true`.

## Workflow

1. Confirm that the task decomposes into independent subtasks; otherwise recommend a single pass or `prompt-chaining-design`.
2. Define the hub contract: input queue, spoke templates, aggregation shape, and coverage-gap shape.
3. Define each spoke with `AgentDefinition(description, prompt, tools, model)` and dispatch via `Task`.
4. Enforce `fresh_session` isolation and `last_message_only` consumption.
5. Define the spoke error contract and local recovery policy.
6. Define valid empty output separately from access failure.
7. Validate the plan offline before presenting it as ready.

## Output Rules

- Reference `assets/isolation-policy.json`, `assets/error-propagation-policy.json`, `assets/aggregation-policy.json`, and `assets/anti-pattern-policy.json`.
- State whether fan-out is justified; do not force subagents onto a single sequential task.
- Never return success with an empty result for an access failure.
- Never allow one spoke failure to abort all unrelated spokes unless the user explicitly requires fail-fast.
- Never claim actual parallel execution occurred unless tool results prove it.

## Scripts

Run:

```bash
python3 skills/subagent-orchestration/scripts/validate_orchestration_plan.py --input <plan.json>
bash skills/subagent-orchestration/scripts/check.sh
```

The validator is offline and rejects shared context, missing `Task` dispatch, missing typed error fields, missing local recovery, missing coverage gaps, fail-fast aggregation, swallowed errors, and false-positive single-pass plans.

## Related Skills

- `katas-hub-and-spoke-isolation`
- `katas-multiagent-error-propagation`
- `structured-output-design`
- `prompt-chaining-design`
- `human-escalation-design`
