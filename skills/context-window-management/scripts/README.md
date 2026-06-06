# Context Window Management Scripts

Validates JSON Context Window Management reports offline.

```bash
bash skills/context-window-management/scripts/check.sh
```

The check accepts valid over-budget and at-limit reports, then rejects
over-budget, P0 eviction, expanding compression, missing preservation, and
missing token estimate reports.
