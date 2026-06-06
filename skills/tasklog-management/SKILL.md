---
name: tasklog-management
author: JM Labs (Javier Montaño)
version: 1.0.0
description: >
  Maintain tasklog.md for cross-session task tracking. Track status, owner, age,
  blockers. Flag stale items. Bridge to workspace/tasks/. [EXPLICIT]
  Trigger: "tasklog", "track task", "open tasks", "task status", "pending items"
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
---

# Tasklog Management

> "Open tasks that never close become invisible technical debt."

## Purpose

Maintains `tasklog.md` as the deterministic cross-session task ledger. Each task
keeps an ID, description, status, owner, opened date, last-update date, optional
bridge path, and notes. Staleness and archival decisions use an explicit
`as_of_date` supplied by the session, not the system clock. [EXPLICIT]

## When to Activate

- The user asks about `tasklog`, open tasks, pending items, task status, stale
  tasks, task closure, or task bridges.
- A session handoff needs tasklog updates or review recommendations.
- A workflow needs `workspace/tasks/TL-NNN-<slug>/` working-file bridges.

Do not activate for generic OS task managers, calendar reminders, browser tasks,
or unrelated project-management advice that does not touch `tasklog.md`.

---

## Deterministic Resources

- `assets/tasklog-contract.json` defines the table schema and required report keys.
- `assets/status-policy.json` defines allowed statuses and transitions.
- `assets/staleness-policy.json` defines stale and archive thresholds using
  explicit `as_of_date`.
- `assets/bridge-policy.json` defines `workspace/tasks/TL-NNN-<slug>/README.md`
  bridge rules.
- `assets/update-report-contract.json` defines the machine-checkable update report.
- `scripts/validate_tasklog_report.py` validates update reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

---

## Procedure

### Step 1: Discover

1. Read `tasklog.md` or mark it missing.
2. Identify the operation: add, update, close, defer, block, stale review,
   archive review, or bridge review.
3. Record the session `as_of_date` as `YYYY-MM-DD`; if absent, mark stale/archive
   age calculations as `[OPEN]` instead of using a hidden clock.

### Step 2: Analyze

1. Validate task IDs with `TL-NNN` format.
2. Validate status against: `open`, `in-progress`, `blocked`, `deferred`,
   `completed`.
3. Validate status transitions through `assets/status-policy.json`.
4. Compute `age_days` from `last_update` to `as_of_date`.
5. Flag active tasks older than 14 days without progress as stale.
6. Mark completed tasks older than 30 days as archive-eligible.
7. Check whether tasks needing working files have a bridge at
   `workspace/tasks/TL-NNN-<slug>/README.md`.

### Step 3: Execute

Allowed writes:

- create or update `tasklog.md`
- create or update `workspace/tasks/TL-NNN-<slug>/README.md`
- move completed items to archive only when explicitly authorized

Rules:

- Do not close, defer, block, archive, or create bridge files without
  authorization.
- Do not invent owners, dates, blockers, or bridge paths.
- Preserve conflicting task evidence and ask for confirmation before writing.

### Step 4: Validate

- IDs use `TL-NNN`.
- Status values and transitions are valid.
- Active items older than 14 days are flagged for review.
- Completed items older than 30 days are archive-eligible.
- Bridge paths match `workspace/tasks/TL-NNN-<slug>/README.md`.
- Machine reports pass `bash skills/tasklog-management/scripts/check.sh`.

## Tasklog Table Contract

```markdown
| ID | Description | Status | Owner | Opened | Last Update | Bridge | Notes |
|---|---|---|---|---|---|---|---|
| TL-015 | Implement offline cache | open | agent | 2026-05-20 | 2026-06-01 | workspace/tasks/TL-015-offline-cache/README.md | Waiting for approval |
```

## Quality Criteria

- [ ] `tasklog.md` was read or missing state was reported.
- [ ] Every task ID matches `TL-NNN`.
- [ ] Every status is allowed and transition-valid.
- [ ] `as_of_date` is explicit for stale/archive calculations.
- [ ] Active tasks older than 14 days are flagged stale.
- [ ] Completed tasks older than 30 days are archive-eligible.
- [ ] Required bridge paths exist or authorized creation is proposed.
- [ ] Writes are authorization-gated.
- [ ] Validator fixtures pass and unsafe reports fail.

## Related Skills

- `session-protocol` — Reviews tasklog during pending closure.
- `session-end-cleanup` — Produces tasklog/changelog update plans.
- `changelog-management` — Records decisions and material project changes.
- `workspace-governance` — Governs `workspace/tasks/` bridge placement.

## Usage

Example invocations:

- `/tasklog-management`
- `Review tasklog.md as of 2026-06-06 and flag stale tasks.`
- `Add TL task for the export validation work and create a bridge if needed.`

## Assumptions & Limits

- Assumes local access to `tasklog.md` and optional `workspace/tasks/**` paths. [EXPLICIT]
- Does not use network calls, randomness, or hidden system time for validation. [EXPLICIT]
- Does not replace owner approval for closing or archiving tasks. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing `tasklog.md` | Report missing; create only when authorized. |
| Bad task ID | Block write and request normalized `TL-NNN` ID. |
| Stale active task | Flag for review; do not auto-close. |
| Completed task >30 days | Mark archive-eligible; archive only when authorized. |
| Bridge missing | Propose deterministic bridge path and create only when authorized. |
