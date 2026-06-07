# AI Content Detection Scripts

## `validate_ai_content_detection_report.py`
Validates a JSON AI content detection report packet offline.

It checks:
- schema and required top-level fields
- evidence ids and signal references
- signal score/weight bounds
- threshold-to-classification consistency
- no unsupported authorship claim
- watermark evidence requirements
- high-stakes human review and non-punitive final actions
- required validation checks

## `check.sh`
Runs the validator against deterministic valid and invalid fixtures.

No network, clock, random, or repository mutation is required.
