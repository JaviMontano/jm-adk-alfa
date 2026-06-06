# Tasklog Management Scripts

Validates JSON Tasklog Management reports offline.

```bash
bash skills/tasklog-management/scripts/check.sh
```

The check accepts valid add and stale-blocked reports, then rejects reports that
omit stale flags, use invalid task IDs, attempt unauthorized writes, or use bad
bridge paths.
