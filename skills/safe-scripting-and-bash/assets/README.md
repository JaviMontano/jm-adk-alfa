# Safe Scripting And Bash Assets

Deterministic assets for safe local Bash script design and review.

- `safe-scripting-and-bash-contract.json`: required report fields and Guardian decisions.
- `write-surface-policy.json`: read/write scope and path requirements.
- `dry-run-policy.json`: dry-run, apply, and force requirements.
- `destructive-command-policy.json`: forbidden shell patterns.
- `portability-policy.json`: Bash portability and tempdir requirements.
- `validation-policy.json`: required offline validation flags.

The offline validator consumes these assets directly.
