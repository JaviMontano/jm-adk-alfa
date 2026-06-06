# Guardrails Management Assets

These assets define deterministic rule capture, confirmation, storage, conflict
review, and offline validation for guardrail operation packets.

- `manifest.json` lists every asset and consumer.
- `rule-schema.json` defines persisted rule fields.
- `classification-policy.json` maps utterances to rule types.
- `confirmation-policy.json` blocks unconfirmed persistence.
- `conflict-policy.json` defines duplicate/conflict handling.
- `storage-map.json` maps rule types to canonical JSON files.
- `report-contract.json` defines the operation packet contract.
