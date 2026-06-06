# Session Manager Scripts

Validates JSON Session Manager reports offline.

```bash
bash skills/session-manager/scripts/check.sh
```

The check accepts valid planned and blocked reports, then rejects reports that
pass with missing context, skip stages, claim implementation without tasks, or
attempt unauthorized persistence.
