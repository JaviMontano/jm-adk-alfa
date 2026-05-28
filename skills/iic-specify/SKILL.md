---
name: iic-specify
description: Creates spec.md with FR-XXX functional requirements, US-X user stories, SC-XXX scenarios. Scores quality 0-10. Traceable requirements. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, specification]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-specify {Metacognition} (v1.0)

> **"A spec without FR-XXX tags is not a spec. It's a wish list."**

## Purpose

Generates structured specifications with traceable requirements. Every requirement gets an ID (FR-XXX), every user story gets an ID (US-X), every scenario gets an ID (SC-XXX). Quality scored 0-10. [EXPLICIT]

**When to use:**
- Starting a new feature or project
- Converting vague requirements into structured specs
- When `/jm:write-spec` is invoked

---

## Core Principles (Immutable Laws)

1. **Law of IDs:** Every requirement MUST have an ID: FR-001, US-1, SC-001. [EXPLICIT]
2. **Law of Testability:** Every FR-XXX must be testable (measurable acceptance criteria). [EXPLICIT]
3. **Law of WHAT-not-HOW:** Specs describe user outcomes, NEVER implementation details (Art. 1.5). [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Elicit
1. **Parse input** (brief, RFP, conversation) for requirements. [EXPLICIT]
2. **Ask clarifying questions** using iic-clarify if ambiguous. [EXPLICIT]
3. **Identify** functional requirements, user stories, scenarios. [EXPLICIT]

### Phase 2: Structure
1. **Assign IDs:** FR-001 through FR-NNN, US-1 through US-N, SC-001 through SC-NNN. [EXPLICIT]
2. **Write acceptance criteria** for each FR in Given/When/Then format. [EXPLICIT]
3. **Cross-reference:** Each US links to FR-XXX tags. Each SC links to US-X. [EXPLICIT]

### Phase 3: Score
1. **Count FR-XXX patterns** (minimum 5 for score > 5). [EXPLICIT]
2. **Check measurable criteria** presence. [EXPLICIT]
3. **Detect unresolved clarifications.**
4. **Score 0-10.** Below 6 = blocked, requires clarification. [EXPLICIT]

---

## 3. Inputs / Outputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements source | Text/File | Yes | Brief, RFP, conversation |

| Output | Type | Description |
|--------|------|-------------|
| spec.md | File | Structured specification |
| Quality score | Number | 0-10 quality rating |

---

## Validation Gate
- [ ] All requirements have FR-XXX IDs
- [ ] All user stories have US-X IDs
- [ ] Acceptance criteria use Given/When/Then
- [ ] No implementation details in spec (phase separation)
- [ ] Quality score ≥ 6

---

## 5. Self-Correction Triggers

> [!WARNING]
> IF spec contains code snippets or tech stack mentions THEN move to plan.md per Art. 1.5.

> [!WARNING]
> IF quality score < 6 THEN invoke iic-clarify before proceeding.

## Usage

Example invocations:

- "/iic-specify" — Run the full iic specify workflow
- "iic specify on this project" — Apply to current context


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
