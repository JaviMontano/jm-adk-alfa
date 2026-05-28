---
name: iic-task-decomposer
description: Decomposes plans into tasks with format [T###] [P?] [US#] Description. Marks parallelizable tasks, tracks dependencies, estimates effort. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, tasks, decomposition]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-task-decomposer {Metacognition} (v1.0)

> **"Every task has an ID, a user story link, and a clear deliverable."**

## Purpose
Converts technical plans into actionable task lists. Format: `- [ ] [T###] [P?] [US#] Description`. Identifies parallelizable tasks [P], dependency chains, and critical path. [EXPLICIT]

**When to use:**
- After plan is approved
- When `/jm:write-user-stories` produces stories

---

## Core Principles
1. **Law of Format:** Every task: `- [ ] [T###] [P?] [US#] Description`. Missing elements = validation failure. [EXPLICIT]
2. **Law of Traceability:** Every task links to at least one US-X from spec. [EXPLICIT]
3. **Law of Parallelism:** Tasks marked [P] can execute simultaneously. Unmarked = sequential. [EXPLICIT]

## Core Process
### Phase 1: Parse Plan
1. Read plan decisions (D1-DN) and task preview. [EXPLICIT]
2. Map decisions to implementation work items. [EXPLICIT]

### Phase 2: Decompose
1. Create T001-TNNN tasks in descending granularity. [EXPLICIT]
2. Mark parallelizable tasks with [P]. [EXPLICIT]
3. Link each to US-X.
4. Identify dependencies between tasks. [EXPLICIT]

### Phase 3: Validate
1. Check all tasks have [T###] and [US#]. [EXPLICIT]
2. Detect circular dependencies. [EXPLICIT]
3. Identify orphan tasks (no US link). [EXPLICIT]
4. Flag critical path. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| plan-*.md | File | Yes | Technical plan |
| spec.md | File | Yes | For US-X linking |

| Output | Type | Description |
|--------|------|-------------|
| tasks.md | File | Decomposed task list |

## Validation Gate
- [ ] All tasks have [T###] format
- [ ] All tasks link to US-X
- [ ] No circular dependencies
- [ ] Critical path identified
- [ ] Parallelizable tasks marked [P]

## 5. Self-Correction Triggers
> [!WARNING]
> IF task has no US-X link THEN flag as orphan — may indicate missing spec coverage.

## Usage

Example invocations:

- "/iic-task-decomposer" — Run the full iic task decomposer workflow
- "iic task decomposer on this project" — Apply to current context


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
