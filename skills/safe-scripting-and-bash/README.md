# Safe Scripting And Bash

Design and review safe, portable, dry-run-first scripts for local agentic development workflows.

## Use It For

- Designing scripts that read, write, move, generate, sync, or validate repo files.
- Reviewing Bash for destructive commands, broad writes, secrets exposure, portability, and rollback.
- Converting risky manual steps into dry-run-first local automation.
- Producing validation commands that run offline and do not mutate user state.

## Deterministic Contract

The canonical JSON report is defined in `assets/safe-scripting-and-bash-contract.json`. It records purpose, write surface, command contract, safety controls, portability controls, validation, and Guardian decision.

## Validation

```bash
bash skills/safe-scripting-and-bash/scripts/check.sh
```

The check executes valid fixtures and rejects invalid mutations for missing dry-run, unsafe destructive patterns, broad writes without force, missing repo-root detection, unsafe tempdirs, secrets exposure, and Guardian inconsistency.
