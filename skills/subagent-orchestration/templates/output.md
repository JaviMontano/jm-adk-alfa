# Subagent Orchestration Output

## Summary

{summary}

## Activation Decision

- Fan-out justified: {yes_no}
- Reason: {reason}
- Single-pass alternative rejected because: {reason}

## Coordinator Contract

- Coordinator id: {coordinator_id}
- Dispatch tool: Task
- Consumes spoke transcript: no
- Consumes last message only: yes

## Spoke Design

| Spoke | Subtarea | Tools | Modelo |
|---|---|---|---|
| {spoke_id} | {subtask} | {tools} | {model} |

## Isolation Contract

- Fresh session per spoke: {yes_no}
- Shared mutable state: none
- Per-spoke tools/model: {yes_no}

## Error contract

- failure_type: {failure_types}
- distingue access_failure vs valid_empty: {yes_no}
- local recovery antes de propagar: {recovery_policy}

## Aggregation

- Partial failure policy: continue_with_coverage_gap
- Coverage gap fields: spoke_id, reason, attempted_query
- Empty success on failure: no

## Validation

- Aislamiento estructural: {check}
- Blast radius acotado: {check}
- access_failure != valid_empty: {check}
- Coverage gap explícito: {check}
- Sin error swallowed como success vacío: {check}
- Offline validator: {check}

## Risks and limits

{risks}
