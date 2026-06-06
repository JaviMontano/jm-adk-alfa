---
name: session-protocol
author: JM Labs (Javier Montaño)
version: 1.1.0
description: >
  Mandatory session initialization: context loading, state recovery, pending closure,
  and next steps proposal. Ensures continuity across AI sessions with zero context loss. [EXPLICIT]
  Constitution Session Protocol section. [EXPLICIT]
  Trigger: "session start", "initialize session", "context recovery", "session protocol", "state recovery"
allowed-tools:
  - Read
  - Write
  - Glob
  - Grep
  - Bash
---

# Session Protocol

> "AI sessions start with zero context. Without a protocol, the first 10 minutes are wasted re-establishing what was done."

## TL;DR

Implements the mandatory session initialization sequence from the Constitution: (1) load context files in order, (2) recover state from recent activity, (3) propose closure for pending items, (4) suggest next steps. Ensures every session starts productive from minute one, with full awareness of project state, open tasks, and recent decisions. [EXPLICIT]

## Deterministic Resources

- `assets/context-load-order.json` defines ordered source loading and missing-file handling.
- `assets/state-recovery-policy.json` defines changelog, tasklog, git, and spec checks.
- `assets/closure-policy.json` defines close/continue/defer/archive recommendation rules.
- `assets/next-step-policy.json` defines next-step ranking and confirmation boundaries.
- `assets/protocol-report-contract.json` defines the report shape validated by `scripts/check.sh`.

## Procedure

### Step 1: Discover — Context Loading
Load in order (read each file):
1. `CLAUDE.md` — project instructions and agent rules
2. `CONSTITUTION.md` or `references/ontology/constitution-v5.2.0.md` — governance
3. `insights/README.md` — insights index (load domain files on-demand)
4. `changelog.md` — recent changes and decisions
5. `tasklog.md` — open tasks and pending work

### Step 2: Analyze — State Recovery
After loading context:
1. Read last 5 `changelog.md` entries — understand recent session outcomes
2. Read all open items in `tasklog.md` — identify pending work, blockers, stale tasks
3. Check `insights/` for any insights tagged `tentative` or `needs validation`
4. Check `git status` and recent commits on current branch
5. Check `.specify/` for any in-progress specs, plans, or debates

### Step 3: Execute — Pending Closure
Before accepting new work:
1. List all open tasks from `tasklog.md` with their age
2. For each: recommend `close` (done), `continue` (active), `defer` (deprioritize), or `archive` (no longer relevant)
3. Flag stale items (>7 days without progress)
4. Present summary to user — confirm before closing or archiving

### Step 4: Validate — Next Steps Proposal
After pending items resolved:
1. Analyze current feature state (IIKit dashboard, branch status, phase progress)
2. Suggest 2-3 concrete next steps ranked by impact
3. Include at least one improvement beyond current task (from insights gaps, constitution TODOs, or observed patterns)
4. Wait for user direction — never start work without explicit confirmation

## Quality Criteria

- [ ] All 5 context files loaded in correct order
- [ ] Last 5 changelog entries reviewed
- [ ] All open tasklog items identified
- [ ] Stale items (>7 days) flagged
- [ ] Pending closure recommendations provided
- [ ] 2-3 next steps proposed with rationale
- [ ] No work started without user confirmation
- [ ] `scripts/check.sh` passes when maintaining this skill
- [ ] Missing context files are reported as `[OPEN]`, not silently skipped
- [ ] Every closure recommendation cites evidence and requires confirmation

## Anti-Patterns

| Anti-Pattern | Why It's Bad | Do This Instead |
|-------------|-------------|-----------------|
| Skipping context loading | Repeat past mistakes, miss decisions | Always load all 5 files |
| Starting work before closure | Task accumulation, invisible debt | Close pending items first |
| Only proposing continuation | Misses improvement opportunities | Include 1 innovation step |
| Auto-closing without user consent | User loses control | Always confirm closures |

## Related Skills

- `continuous-learning` — Insights loaded during context recovery
- `tasklog-management` — Tasklog is primary input for pending closure
- `changelog-management` — Changelog is primary input for state recovery

## Usage

Example invocations:

- "/session-protocol" — Run the full session protocol workflow
- "session protocol on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|----------|----------|
| Empty or minimal input | Request clarification before proceeding |
| Conflicting requirements | Flag conflicts explicitly, propose resolution |
| Out-of-scope request | Redirect to appropriate skill or escalate |
