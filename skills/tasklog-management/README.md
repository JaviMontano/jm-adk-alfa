# Tasklog Management

`tasklog-management` maintains `tasklog.md` as a reproducible cross-session task
ledger. It validates IDs, statuses, dates, stale review, archive eligibility,
and task bridges before any write.

## Triggers

- `tasklog-management`
- `tasklog`
- `track task`
- `open tasks`
- `task status`
- `pending items`
- `stale tasks`

## Allowed Tools

- Read
- Write
- Edit
- Glob
- Grep
- Bash

## Deterministic Assets

| Asset | Purpose |
|---|---|
| `assets/tasklog-contract.json` | Tasklog table columns and report shape. |
| `assets/status-policy.json` | Allowed statuses and transitions. |
| `assets/staleness-policy.json` | 14-day stale and 30-day archive rules using explicit `as_of_date`. |
| `assets/bridge-policy.json` | Deterministic `workspace/tasks/TL-NNN-<slug>/README.md` bridge paths. |
| `assets/update-report-contract.json` | Machine-checkable update report requirements. |

## Output Format

Return Markdown with:

- tasklog snapshot
- requested operation
- task updates
- stale review
- bridge review
- archive review
- proposed writes
- Guardian decision

Machine-readable reports should pass:

```bash
bash skills/tasklog-management/scripts/check.sh
```

## Safety Rules

- Do not compute stale or archive status without explicit `as_of_date`.
- Do not close, archive, or create bridge files without authorization.
- Do not invent owners, blockers, or dates.
- Do not activate for unrelated "task manager" questions.
