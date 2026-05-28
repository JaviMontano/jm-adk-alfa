---
name: iic-bugfix
description: Structured bug tracking. Creates bug entries with severity, reproduction steps, and T-B tasks. Links to affected requirements. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, bugs, tracking]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-bugfix {Metacognition} (v1.0)

> **"A bug without reproduction steps is not a bug report. It's a rumor."**

## Purpose
Creates structured bug entries in bugs.md with severity, reproduction steps, and assigned T-B tasks. Links bugs to affected FR-XXX requirements. [EXPLICIT]

**When to use:**
- When a bug is discovered during implementation or testing
- When `/jm:repair` is invoked

---

## Core Principles
1. **Law of Structure:** Bug format: ID, severity, reproduction, affected FR-XXX, assigned T-B task. [EXPLICIT]
2. **Law of Traceability:** Every bug links to affected requirements. [EXPLICIT]
3. **Law of Tasks:** Every bug gets a T-B### task in tasks.md. [EXPLICIT]

## Core Process
### Phase 1: Document Bug
1. Assign bug ID (BUG-NNN). [EXPLICIT]
2. Record: severity (critical/high/medium/low), reproduction steps, expected vs actual. [EXPLICIT]
3. Link to affected FR-XXX/US-X. [EXPLICIT]

### Phase 2: Create Fix Task
1. Add `- [ ] [T-B###] [BUG-NNN] Fix: {description}` to tasks.md. [EXPLICIT]
2. If test assertion needs update → re-specify via iic-testify (not direct edit). [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Bug description | Text | Yes | What went wrong |

| Output | Type | Description |
|--------|------|-------------|
| bugs.md entry | File | Structured bug report |
| tasks.md update | File | T-B### fix task |

## Validation Gate
- [ ] Bug has reproduction steps
- [ ] Linked to affected FR-XXX
- [ ] Fix task created in tasks.md

## Usage

Example invocations:

- "/iic-bugfix" — Run the full iic bugfix workflow
- "iic bugfix on this project" — Apply to current context


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
