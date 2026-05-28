---
name: workflow-forge
description: Creates new workflows (slash commands) following the Antigravity format with phases, agent coordination, and verification checkpoints. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [core, forge, workflow, scaffold]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# workflow-forge {Core} (v1.0)

> **"A workflow is a choreography. Every agent knows its entrance, its solo, and its exit."**

## Purpose

Factory for creating new workflows (slash commands) in the kit. Produces workflow `.md` files that coordinate agents through phases with verification checkpoints. [EXPLICIT]

**When to use:**

- Creating a new slash command workflow
- Standardizing an ad-hoc process into a repeatable workflow
- Extending the kit with new automation sequences

---

## Core Principles (Immutable Laws)

1. **Law of Phases:** Every workflow has 2+ phases. Phase 1 is always clarification/planning. Final phase is always verification. [EXPLICIT]
2. **Law of Agents:** Every phase declares which agents execute it. No anonymous work. [EXPLICIT]
3. **Law of Checkpoints:** Between phases, a verification step validates output before proceeding. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Intent Mapping

1. **Identify the trigger:** What slash command activates this workflow? (`/jm:{command}`)
2. **Map the outcome:** What deliverable does this workflow produce?
3. **List participating agents:** Which agents from the 101-agent roster are involved?

### Phase 2: Phase Design

1. **Phase 1 (Clarification):** Agent asks qualifying questions before proceeding. [EXPLICIT]
2. **Phase 2-N (Execution):** Sequential or parallel agent work with clear inputs/outputs. [EXPLICIT]
3. **Final Phase (Verification):** Quality gate check against defined criteria. [EXPLICIT]

### Phase 3: Assembly

1. **Write the workflow .md** with frontmatter (description, command, skills_involved, agents_coordinated). [EXPLICIT]
2. **Define inputs/outputs** for each phase. [EXPLICIT]
3. **Add example execution** showing a sample dialogue. [EXPLICIT]

---

## 3. Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Workflow Name | Text | Yes | Kebab-case command name |
| Description | Text | Yes | One-line purpose |
| Agents | List | Yes | Agent names involved |
| Skills | List | Yes | Skills loaded during execution |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| `workflows/{name}.md` | File | Workflow definition |

---

## Validation Gate (10x Checklist)

- [ ] **Frontmatter:** Has description, command, skills_involved, agents_coordinated
- [ ] **Phases:** Minimum 2 phases with clear boundaries
- [ ] **Verification:** Final phase includes quality check
- [ ] **Example:** Contains sample execution dialogue
- [ ] **Stack Compliance:** No AWS/Azure/Docker references (R-002, R-003)

---

## 5. Edge Cases & Antipatterns

### Antipatterns

- **Monolithic:** Single-phase workflow with no checkpoints → **BAD**
- **Agentless:** Workflow that doesn't declare participating agents → **BAD**

### Edge Cases

- **Single-agent workflow:** Still requires 2+ phases (clarify → execute → verify).
- **Cross-mode workflow:** Workflows that span analysis and development (like `full-lifecycle`) must declare mode transitions.

---

## 6. Self-Correction Triggers

> [!WARNING]
> IF workflow has no verification phase THEN **STOP**. Add a quality gate as the final phase.

> [!WARNING]
> IF workflow references non-existent agents or skills THEN **STOP**. Cross-reference against the agent/skill catalog.

## Usage

Example invocations:

- "/workflow-forge" — Run the full workflow forge workflow
- "workflow forge on this project" — Apply to current context


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
