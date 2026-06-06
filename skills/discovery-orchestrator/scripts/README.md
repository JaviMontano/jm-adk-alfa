# Discovery Orchestrator Scripts

## `validate_discovery_orchestrator_packet.py`

Validates a JSON orchestration packet against the local assets:

- top-level packet contract;
- phase order and required phases;
- canonical discovery skill sequence;
- G1, G1B, G2, and G3 gate policies;
- non-analysis, no-price, and no-downstream-execution boundaries;
- exact dates and evidence tags.

## `check.sh`

Runs deterministic fixtures offline. It accepts valid packets and rejects invalid packets that analyze content, skip approval, break phase order, use a non-canonical skill, omit the assumption warning, or leak prices.
