# Assumption Log Knowledge Graph

## Core Nodes

- `assumption-log`: read-only skill for assumption tracking.
- `activation-policy`: positive, negative, and clarification routing.
- `status-policy`: ID, status, impact, and risk taxonomy.
- `evidence-policy`: accepted evidence tags and proof requirements.
- `log-contract`: required output sections and fields.
- `offline-validator`: deterministic report validation script.
- `validation-queue`: required output for high-impact open assumptions.

## Relationships

- The skill uses activation, status, and evidence policies.
- The skill produces a log that must match the contract.
- The validator checks the contract and policy requirements.
- High-impact open assumptions require validation queue entries.
