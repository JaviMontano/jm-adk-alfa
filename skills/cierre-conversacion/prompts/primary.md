# Cierre Conversacion Primary Prompt

## Objective

Produce a deterministic closeout packet for the current conversation.

## Required Inputs

- Current objective and scope.
- Work completed, files touched, PRs, commands, or artifacts.
- Decisions, risks, blockers, and open tasks.
- Authority status for durable writes.

## Process

1. Classify the trigger.
2. Harvest evidence-backed facts.
3. Build the packet in the template order.
4. Mark unverified items `[POR_CONFIRMAR]`.
5. Block false completion when validation or authority is missing.

## Output

Markdown with summary, completed work, decisions, open tasks, learnings, risks, validation, durable update plan, next handoff, and Guardian decision.
