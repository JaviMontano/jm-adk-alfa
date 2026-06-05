# Repo Sync Auditor

Read-only repository truth audit for safe PR work.

Use it before resuming a long-running deployment, applying a patch, creating a
branch, or telling a user what is really deployed. The bundled script reports
branch state, dirty files, ledger drift, review-doc coverage, deterministic
script coverage, generated-file dirtiness, and recommended next actions.

## Commands

```bash
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format markdown
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format json
bash skills/repo-sync-auditor/scripts/check.sh
```

The script does not fetch, rebase, reset, clean, push, or write files.
