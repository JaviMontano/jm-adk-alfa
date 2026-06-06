---
name: session-manager
description: Manages session state, pipeline progress, and cold-start priming. Reads/writes .specify/context.json to track feature stages and artifact completion. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [core, session, state, pipeline]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# session-manager {Core} (v1.0)

> **"Every session knows where it left off. Every feature knows its stage."**

## Purpose

Tracks pipeline progress across sessions using `.specify/context.json`.
Computes feature stage from real artifacts, primes cold starts from known
sources, and persists state only with evidence-backed authorization. [EXPLICIT]

## When to Activate

- A session starts and needs project state, last plan, active tasks, and next action.
- A user asks for `/jm:status`, session status, context recovery, or pipeline progress.
- A phase finishes and `.specify/context.json`, `.specify/score-history.json`, or
  `.specify/decisions/` may need an authorized update.

Do not activate for unrelated account, password, browser, weather, calendar, or
generic "session" questions that do not involve project pipeline state. [EXPLICIT]

---

## Deterministic Resources

- `assets/state-contract.json` defines required status-report fields and allowed
  context states.
- `assets/stage-policy.json` defines allowed stages, artifact evidence, and
  no-skip stage progression.
- `assets/priming-policy.json` defines cold-start read order and missing-source
  handling.
- `assets/persistence-policy.json` defines authorized writes to `.specify/**`.
- `assets/source-boundary-policy.json` defines allowed source and output paths.
- `scripts/validate_session_manager_report.py` validates JSON reports offline.
- `scripts/check.sh` runs deterministic positive and negative fixtures.

---

## Core Principles (Immutable Laws)

1. **Law of State:** `.specify/context.json` is the project state source of truth
   after it is read and validated. [EXPLICIT]
2. **Law of Stages:** Feature stages progress linearly: `specified` -> `planned`
   -> `testified` -> `tasks-ready` -> `implementing` -> `complete`. [EXPLICIT]
3. **Law of Priming:** New sessions must read `.specify/context.json`, the latest
   plan, and active tasks before proposing work. [EXPLICIT]
4. **Law of Evidence:** Every stage, blocker, write, and next action must cite a
   local artifact or mark the gap as `[OPEN]`. [EXPLICIT]
5. **Law of Authorized Persistence:** Never write state from defaults, guesses, or
   stale memory; writes require artifact evidence and explicit process
   authorization. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Cold-Start Priming

1. Read `.specify/context.json` and record `present`, `missing`, or `invalid`.
2. Read the latest `.specify/plans/plan-*.md` by filename/date order when present.
3. Read active tasks from `tasks.md` or `.specify/tasks.md` when present.
4. Record all loaded and missing sources in order with evidence tags.
5. If the context file is missing or invalid, block persistence and ask for
   recovery input unless an existing repo policy authorizes initialization.

### Phase 2: Stage Computation

Compute the stage from artifact evidence:

| Evidence | Stage |
|---|---|
| `spec.md` exists | `specified` |
| `plan-*.md` exists | `planned` |
| `tests/features/*.feature` exists | `testified` |
| `tasks.md` or `.specify/tasks.md` exists | `tasks-ready` |
| task evidence shows partial implementation | `implementing` |
| all task evidence is complete and validation evidence exists | `complete` |

Rules:

- Do not advance more than one stage in one session-manager pass.
- Do not report `implementing` unless task evidence exists and progress is
  between 1 and 99 percent.
- Do not report `complete` unless task evidence is complete and validation
  evidence is present.
- If artifacts contradict `context.json`, preserve both values and block
  persistence until the user confirms the correction.

### Phase 3: State Persistence

1. Update `.specify/context.json` only after the computed stage is verified and
   the write is authorized.
2. Append `.specify/score-history.json` only after a named gate pass is present.
3. Create `.specify/decisions/DL-NNN.md` only after a concrete decision exists.
4. Refuse writes outside `.specify/context.json`, `.specify/score-history.json`,
   and `.specify/decisions/`.

### Phase 4: Status Report

Return a concise report with:

- context snapshot and source statuses
- computed stage and previous recorded stage
- artifact evidence
- persistence actions or blocked writes
- next action
- Guardian decision

---

## Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|---|---|---:|---|
| `.specify/context.json` | JSON | Yes | Project state file and recorded stage. |
| `.specify/plans/plan-*.md` | Markdown | No | Latest plan evidence. |
| `tasks.md` or `.specify/tasks.md` | Markdown | No | Task and implementation evidence. |
| `tests/features/*.feature` | Gherkin | No | Testification evidence. |
| `.specify/score-history.json` | JSON | No | Gate pass history. |

### Outputs

| Output | Type | Description |
|---|---|---|
| Status report | Markdown | Current state, computed stage, blockers, and next step. |
| Updated context | JSON | Authorized `.specify/context.json` update only when safe. |
| Decision log | Markdown | Authorized `.specify/decisions/DL-NNN.md` when a decision exists. |
| Machine report | JSON | Optional report accepted by `scripts/validate_session_manager_report.py`. |

---

## Validation Gate (10x Checklist)

- [ ] `.specify/context.json` was read or marked missing/invalid with `[OPEN]`.
- [ ] Latest plan and active tasks were read or marked missing with `[OPEN]`.
- [ ] Computed stage cites artifact evidence and follows `assets/stage-policy.json`.
- [ ] No stage skip occurred without Guardian block.
- [ ] `implementing` and `complete` stages have task/validation evidence.
- [ ] Persistence actions stay inside `.specify/**` allowed targets.
- [ ] Writes are authorized before any state file changes.
- [ ] Output includes next action and Guardian decision.
- [ ] Machine report passes `bash skills/session-manager/scripts/check.sh` when used.

---

## Self-Correction Triggers

> [!WARNING]
> IF `.specify/context.json` is missing THEN do not silently create it. Block,
> report the missing source, and initialize only when a repo policy or user
> confirmation authorizes the write.

> [!WARNING]
> IF stage is `implementing` but no task file exists THEN block and roll back the
> computed stage to the latest evidence-backed stage.

> [!WARNING]
> IF context stage and artifact stage conflict THEN preserve both values, explain
> the conflict, and request confirmation before persistence.

## Usage

Example invocations:

- `/jm:status`
- `Run session-manager for this repo and show the next action.`
- `Update context.json after this phase completion if the evidence is valid.`

## Assumptions & Limits

- Assumes local access to `.specify/**` and related project artifacts. [EXPLICIT]
- Does not infer progress from memory, conversation history, branch names, or
  elapsed time. [EXPLICIT]
- Does not replace project owner confirmation for conflicting or destructive
  state changes. [EXPLICIT]

## Edge Cases

| Scenario | Handling |
|---|---|
| Missing context file | Block persistence and request recovery authorization. |
| Invalid JSON context | Report parse failure and avoid writes. |
| Plan exists but no spec | Compute the lowest consistent evidence-backed stage and block skip. |
| Tasks complete but no validation evidence | Report `implementing` or block `complete`. |
| Unrelated "session" request | Do not activate. |
