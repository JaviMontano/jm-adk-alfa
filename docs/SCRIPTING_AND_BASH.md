# Scripting And Bash

## Purpose

Alfa scripts should be safe to run in local developer environments and clear about the files they may touch.

## Script Rules

- Detect repo root with `git rev-parse --show-toplevel` or an equivalent `git -C` lookup.
- Use dry-run by default when a script may create, move, or write many files.
- Require `--apply` or an equally explicit flag for writes.
- Require `--force` for overwrites.
- Never read, print, or store `.env*`, credentials, tokens, keys, or private secrets.
- Avoid destructive commands such as hard resets, broad deletes, or force pushes.
- Print clear status and exit nonzero on blocking errors.

## Validation

Use:

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh scripts/adapters/*.sh
```

Run behavior-specific smoke tests before handoff.
