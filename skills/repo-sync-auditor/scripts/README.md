# Repo Sync Auditor Scripts

`audit-repo-sync.py` emits a read-only audit of local repository state.

```bash
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format markdown
python3 skills/repo-sync-auditor/scripts/audit-repo-sync.py --format json
bash skills/repo-sync-auditor/scripts/check.sh
```

The script uses local refs only. It does not fetch, write, rebase, reset, push,
or clean files.
