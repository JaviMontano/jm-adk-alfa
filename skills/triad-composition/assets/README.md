# Triad Composition Assets

Deterministic assets for selecting Lead, Support, and Guardian from PRISTINO's triad composition contract.

- `composition-matrix.json`: canonical domain-to-triad matrix.
- `classification-policy.json`: confidence thresholds, tie-breakers, and execution-mode routing.
- `degraded-mode-policy.json`: explicit fallback behavior when a triad member fails.
- `triad-output-contract.json`: machine-readable output packet contract.

Use these assets before producing a triad recommendation, then validate sample packets with `scripts/validate_triad_packet.py`.
