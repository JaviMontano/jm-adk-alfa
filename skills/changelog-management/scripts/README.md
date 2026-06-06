# Changelog Management Scripts

Validates JSON Changelog Management reports offline.

```bash
bash skills/changelog-management/scripts/check.sh
```

The check accepts valid decision and duplicate-block reports, then rejects
unsupported types, future dates, duplicate append, missing principles, and
unauthorized entries.
