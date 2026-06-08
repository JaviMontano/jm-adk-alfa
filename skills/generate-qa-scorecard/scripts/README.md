# Generate QA Scorecard Scripts

## `validate_qa_scorecard.py`

Validates a structured JSON QA scorecard against the local assets contract.

## `check.sh`

Runs deterministic fixtures:

- `valid-*.json` must pass.
- `invalid-*.json` must fail.

The check is offline and does not call external services.
