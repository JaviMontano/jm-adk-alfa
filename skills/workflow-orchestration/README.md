<!--
generated-by: scripts/scaffold-skill.py
generated-for: workflow-orchestration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Workflow Orchestration

Multi-step workflow execution with checkpoint and resume capability.

## Triggers

- workflow-orchestration

## Allowed Tools

- Read
- Write
- Glob
- Grep
- Bash

## Quick Use

Use this skill when the request needs a resumable execution plan with stage checkpoints, durable state, retry policy, and observability.

## Output Format

Markdown orchestration plan with objective, trigger, agents, inputs, stages, resume contract, observability, and completion criteria.

## Deterministic Compiler

```bash
python3 skills/workflow-orchestration/scripts/compile-orchestration-plan.py \
  --input skills/workflow-orchestration/scripts/fixtures/product-launch-orchestration.json
```
