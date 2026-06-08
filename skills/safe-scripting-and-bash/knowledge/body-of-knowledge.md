# Safe Scripting And Bash Body of Knowledge

## Canon

Safe local scripts make their write surface explicit, default to dry-run when writes are possible, detect the repo root dynamically, avoid user-specific absolute paths, quote variables, use safe temp directories, and fail closed on ambiguous or destructive behavior.

## Required Script Safety Shape

- **Purpose:** one concrete operation with known inputs and outputs.
- **Write surface:** read-only, narrow, or broad; broad writes require stronger review.
- **Command contract:** entrypoint, flags, default mode, apply mode, force mode, and exit codes.
- **Dry-run:** default for any script that writes, moves, deletes, syncs, or overwrites files.
- **Repo root:** use `git rev-parse --show-toplevel` or an equivalent local anchor.
- **Destructive commands:** block `rm -rf`, `git reset --hard`, `git clean -fd`, `sudo`, and force push unless a human explicitly approves a confined operation.
- **Portability:** Bash shebang, `set -euo pipefail`, quoted variables, `mktemp -d`, cleanup trap, and no GNU-only assumptions without guards.
- **Validation:** `bash -n`, deterministic fixture smoke test, no network requirement, and no secrets printed.

## Quality Signals

| Signal | Target |
|---|---|
| Dry-run default | Writes are only planned unless `--apply` is explicit |
| Write surface | Paths and overwrite rules are declared |
| Destructive guard | Dangerous patterns are blocked or explicitly escalated |
| Portability | Bash mode, quoting, tempdir, and repo-root detection are present |
| Validation | Syntax and fixture smoke tests run offline |

## Anti-Patterns

- Hidden write behavior in a script that appears read-only.
- User-specific absolute paths such as `/Users/name/project`.
- `rm -rf`, `sudo`, hard reset, or force push in reusable scripts.
- Broad overwrites without `--force`.
- Dry-run mode that still mutates files.
