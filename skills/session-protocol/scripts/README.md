# Session Protocol Scripts

Validates JSON Session Protocol reports offline.

```bash
bash skills/session-protocol/scripts/check.sh
```

The check accepts valid reports and rejects reports that auto-close tasks,
omit context loading, or start work before confirmation.
