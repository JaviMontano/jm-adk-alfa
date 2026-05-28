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

Tracks pipeline progress across sessions using `.specify/context.json`. Manages feature stage computation (specified → planned → testified → tasks-ready → implementing → complete) and provides cold-start priming for new sessions. [EXPLICIT]

**When to use:**

- Session initialization (cold-start priming)
- After each phase completion (stage advancement)
- When `/jm:status` is invoked

---

## Core Principles (Immutable Laws)

1. **Law of State:** `.specify/context.json` is the single source of truth for project state. [EXPLICIT]
2. **Law of Stages:** Feature stages progress linearly: specified → planned → testified → tasks-ready → implementing-NN% → complete. [EXPLICIT]
3. **Law of Priming:** New sessions must read context.json + last plan + active tasks before starting work. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Cold-Start Priming

1. **Read `.specify/context.json`** — project state, active features, stage. [EXPLICIT]
2. **Read latest plan** in `.specify/plans/` — most recent plan-FECHA-TAREA.md. [EXPLICIT]
3. **Read active tasks** — tasks.md if exists. [EXPLICIT]
4. **Present status** to user: "Project at stage {X}. Last plan: {Y}. Active tasks: {N}."

### Phase 2: Stage Computation

1. **Check artifact existence:**
   - spec.md → `specified`
   - plan-*.md → `planned`
   - tests/features/*.feature → `testified`
   - tasks.md → `tasks-ready`
   - Implementation progress → `implementing-NN%`
   - All tasks complete → `complete`
2. **Update context.json** with computed stage. [EXPLICIT]
3. **Suggest next action** using the stage progression table. [EXPLICIT]

### Phase 3: State Persistence

1. **After each phase completion**, update context.json stage field. [EXPLICIT]
2. **After each gate pass**, log in score-history.json. [EXPLICIT]
3. **After each decision**, create DL-NNN.md in `.specify/decisions/`. [EXPLICIT]

---

## 3. Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| context.json | JSON | Yes | Project state file |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| Status report | Text | Current stage + next steps |
| Updated context.json | JSON | Persisted state changes |

---

## Validation Gate (10x Checklist)

- [ ] **context.json read** at session start
- [ ] **Stage computed** from artifact existence
- [ ] **Next action suggested** based on stage
- [ ] **State persisted** after each phase change

---

## 5. Self-Correction Triggers

> [!WARNING]
> IF context.json is missing THEN create it with initial state from CONSTITUTION.md defaults.

> [!WARNING]
> IF stage is "implementing" but no tasks.md exists THEN **STOP**. Roll back to "planned" stage.

## Usage

Example invocations:

- "/session-manager" — Run the full session manager workflow
- "session manager on this project" — Apply to current context


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
