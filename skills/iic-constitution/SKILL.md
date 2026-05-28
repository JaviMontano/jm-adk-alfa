---
name: iic-constitution
description: Governance backbone. Loads CONSTITUTION.md, validates all actions against non-negotiable principles. Blocks constitutional violations. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, governance]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-constitution {Metacognition} (v1.0)

> **"The Constitution is supreme. No skill, no agent, no workflow overrides it."**

## Purpose

Loads and enforces CONSTITUTION.md principles across all kit operations. Validates that outputs comply with evidence tagging, stack constraints, phase separation, and confidence thresholds. [EXPLICIT]

**When to use:**
- Implicitly active on every kit operation
- Explicitly when validating constitutional compliance
- When resolving conflicts between skills or rules

---

## Core Principles (Immutable Laws)

1. **Law of Supremacy:** CONSTITUTION.md overrides all skills, rules, and workflows. No exception. [EXPLICIT]
2. **Law of Phase Separation:** Each artifact answers ONE question (why/what/how/work/code). Content in wrong phase = violation. [EXPLICIT]
3. **Law of Traceability:** Every requirement traceable from spec → plan → tasks → tests → code. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Load Constitution
1. **Read CONSTITUTION.md** — internalize Articles 1-5. [EXPLICIT]
2. **Extract active constraints:** stack policy, confidence threshold, evidence tags, gates. [EXPLICIT]

### Phase 2: Validate
1. **Check output** against each Article. [EXPLICIT]
2. **Flag violations** with article reference: "Violates Art. 1.4 (Firebase-First)". [EXPLICIT]
3. **Block** if critical violation. **Warn** if minor. [EXPLICIT]

---

## 3. Inputs / Outputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| CONSTITUTION.md | File | Yes | Governance document |
| Output to validate | Any | Yes | Skill output to check |

| Output | Type | Description |
|--------|------|-------------|
| Compliance report | Text | Pass/fail per article |

---

## Validation Gate
- [ ] Constitution loaded before validation
- [ ] Each article checked independently
- [ ] Violations reference specific article number
- [ ] Critical violations block advancement
- [ ] Phase separation verified (no content leakage)

---

## 5. Self-Correction Triggers

> [!WARNING]
> IF output references AWS/Azure THEN block per Art. 1.4.

> [!WARNING]
> IF spec.md contains implementation details THEN flag phase separation violation per Art. 1.5.

## Usage

Example invocations:

- "/iic-constitution" — Run the full iic constitution workflow
- "iic constitution on this project" — Apply to current context


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
