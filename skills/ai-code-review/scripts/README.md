# AI Code Review Scripts

## `validate_ai_code_review_report.py`
Validates a JSON AI Code Review report packet offline.

It checks:
- schema and required top-level fields
- scope include/exclude matching
- evidence tags and evidence references
- finding priority, status, confidence, file, and line
- high-priority false-positive controls
- test-status claims against recorded command evidence
- required validation checks

## `check.sh`
Runs the validator against deterministic valid and invalid fixtures.

No network, clock, random, or repository mutation is required.
