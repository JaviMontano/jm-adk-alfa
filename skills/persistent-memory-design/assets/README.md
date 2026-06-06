# Persistent Memory Design Assets

Deterministic contracts for persistent scratchpad design. These assets define the offline evidence required before a durable memory report is accepted: safe path, fixed sections, evidence per entry, read-once access, idempotent writes, compact recovery, and JSON report shape.

Use `manifest.json` as the index and `report-contract.json` with `scripts/validate_persistent_memory_report.py` for fixture validation.
