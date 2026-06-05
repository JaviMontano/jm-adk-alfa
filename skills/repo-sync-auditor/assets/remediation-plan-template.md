# Repo Sync Remediation Plan

## Safe Baseline

- Confirm branch and `HEAD`.
- Confirm local `origin/main`.
- Confirm dirty-tree state before editing.

## Drift Repair

- Reconcile ledger rows only in a dedicated PR when the delta is broad.
- Keep skill package PRs scoped to one skill plus generated indexes.
- Regenerate adapters and `PRISTINO-INDEX.md` only after reviewing diffs.

## Deployment Evidence

- Treat merged PRs and files present in `origin/main` as deployment evidence.
- Treat draft/staging PRs as checkpoints, not deployed code.
