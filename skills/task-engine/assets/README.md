# Task Engine Assets

Deterministic assets for applying DSVSR without fake certainty.

- `activation-policy.json`: full DSVSR vs fast path routing.
- `confidence-scale.json`: score bands and evidence requirements.
- `dsvsr-packet-contract.json`: required packet sections and blocked phrases.
- `reflection-policy.json`: retry limits and uncertainty handling.

Use these assets before producing DSVSR output, then validate examples with `scripts/validate_dsvsr_packet.py`.
