---
name: iic-core-engine
description: State machine and next-step guidance. Computes feature stage from artifacts. Suggests next action. Updates context.json. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, state-machine, engine]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-core-engine {Metacognition} (v1.0)

> **"I know where you are. I know where you should go next."**

## Purpose
Central state machine. Computes project stage from artifact existence. Suggests the next skill/workflow to invoke. Single source of truth for workflow progression. [EXPLICIT]

**When to use:**
- Session start (cold-start priming)
- When `/jm:status` is invoked
- After any phase completion

---

## Core Principles
1. **Law of State:** context.json is the single source of truth. [EXPLICIT]
2. **Law of Stages:** specified → planned → testified → tasks-ready → implementing-NN% → complete. [EXPLICIT]
3. **Law of Suggestion:** Always recommend next action based on current stage. [EXPLICIT]

## Core Process
### Phase 1: Compute Stage
1. Check artifact existence:
   - spec.md exists → `specified`
   - plan-*.md exists → `planned`
   - *.feature files exist → `testified`
   - tasks.md exists → `tasks-ready`
   - Implementation progress → `implementing-NN%`
   - All tasks complete → `complete`

### Phase 2: Suggest Next
| Stage | Next Action |
|-------|-------------|
| (none) | `/jm:write-spec` → create spec.md |
| specified | `/jm:design-architecture` → create plan |
| planned | iic-testify → create .feature files |
| testified | iic-task-decomposer → create tasks.md |
| tasks-ready | iic-implement → start coding |
| implementing | Continue tasks, run tests |
| complete | `/jm:deploy-firebase` or `/jm:deploy-hostinger` |

### Phase 3: Update State
1. Update context.json stage field. [EXPLICIT]
2. Log transition in score-history.json. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| context.json | JSON | Yes | Current state |
| Project artifacts | Files | Yes | For stage computation |

| Output | Type | Description |
|--------|------|-------------|
| Status report | Text | Stage + next action |
| context.json update | JSON | Updated stage |

## Validation Gate
- [ ] Stage computed from actual artifact existence
- [ ] Next action maps to valid skill/workflow
- [ ] context.json updated after state change

## Usage

Example invocations:

- "/iic-core-engine" — Run the full iic core engine workflow
- "iic core engine on this project" — Apply to current context


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
