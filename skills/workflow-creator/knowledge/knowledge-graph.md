# Workflow Creator Knowledge Graph

## Core Concepts

- workflow-definition-contract: 17 top-level workflow fields
- step-contract: 12 fields per step
- activation-policy: activate, decline, clarify, and offline rules
- quality-gates: fail-closed checks for workflow outputs
- deterministic-validator: local JSON validator and fixtures

## Dependencies

- Upstream: user intent, owning skill context, local catalog evidence
- Downstream: release packet, workflow YAML, review evidence, validation logs

## Relationships

- `workflow-creator` produces `workflow-definition`
- `workflow-definition` is validated by `workflow-definition-contract`
- `step-contract` is validated by `deterministic-validator`
- `quality-gates` block `ledger-completion`
- `activation-policy` blocks false-positive routing
