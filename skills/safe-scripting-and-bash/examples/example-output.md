# Example Output

## Summary

Safe adapter update script plan: dry-run-first, repo-root aware, no destructive shell patterns, explicit `--apply`, explicit `--force` for overwrites, and deterministic offline validation.

## Contract

- Write surface: `generated/adapters/**`, narrow scope.
- Default mode: dry-run.
- Apply mode: `--apply` required.
- Overwrite mode: `--force` required when target exists.
- Repo root: `git rev-parse --show-toplevel`.
- Tempdir: `mktemp -d` with cleanup trap.
- Network: forbidden.
- Secrets: never printed or persisted.

## Validation Command

```bash
bash -n scripts/update-adapters.sh
bash scripts/update-adapters.sh --dry-run --fixture tests/fixtures/adapters
```

## Validation

- Dry-run default: yes.
- Apply requires flag: yes.
- Force requires flag: yes.
- Dangerous commands blocked: yes.
- Offline validator: `skills/safe-scripting-and-bash/scripts/check.sh`.
