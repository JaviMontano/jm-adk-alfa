# GitHub Actions CI/CD Scripts

## `validate_github_actions_ci.py`

Validates a structured JSON workflow plan against the local assets contract.

## `check.sh`

Runs deterministic fixtures:

- `valid-*.json` must pass.
- `invalid-*.json` must fail.

The check is offline and does not call GitHub.
