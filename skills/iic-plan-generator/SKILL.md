---
name: iic-plan-generator
description: Creates plan-YYYY-MM-DD-{task}.md with decision table (D1-DN), technical approach, Firebase services, and fact-checked viability. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, planning]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-plan-generator {Metacognition} (v1.0)

> **"Every plan has a decision table. Every decision has a rationale."**

## Purpose

Generates technical plans from specifications. Each plan includes a numbered decision table (D1-DN), Firebase service selection, task preview, and fact-checked viability assessment via internet search. [EXPLICIT]

**When to use:**
- After spec.md is approved (post-G1)
- When `/jm:design-architecture` is invoked
- For any task requiring technical planning

---

## Core Principles (Immutable Laws)

1. **Law of Decisions:** Every plan contains a decision table. No decision without scope and rationale. [EXPLICIT]
2. **Law of Fact-Check:** Technical viability validated via WebSearch before plan approval. Confidence ≥ 0.95. [EXPLICIT]
3. **Law of Firebase:** All technical decisions constrained to Firebase/Google/Hostinger stack (Art. 1.4). [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Analyze Spec
1. **Read spec.md** — extract FR-XXX requirements. [EXPLICIT]
2. **Identify technical decisions** needed (database, auth, API, hosting). [EXPLICIT]
3. **Map FR-XXX to Firebase services.**

### Phase 2: Research + Fact-Check
1. **WebSearch** for each technical decision: "Firebase [service] best practices 2026". [EXPLICIT]
2. **Validate viability** within Hostinger constraints. [EXPLICIT]
3. **Score confidence** per decision. Overall must reach ≥ 0.95. [EXPLICIT]

### Phase 3: Draft Plan
1. **Write plan-YYYY-MM-DD-{task}.md** using TEMPLATE from `.specify/plans/`. [EXPLICIT]
2. **Populate decision table** D1 through DN with scope + rationale. [EXPLICIT]
3. **List Firebase services** used (checkbox format). [EXPLICIT]
4. **Preview tasks** (T001-T00N) for iic-task-decomposer. [EXPLICIT]
5. **Create ADR** for significant architectural decisions. [EXPLICIT]

---

## 3. Inputs / Outputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| spec.md | File | Yes | Approved specification |

| Output | Type | Description |
|--------|------|-------------|
| plan-YYYY-MM-DD-{task}.md | File | Technical plan in .specify/plans/ |
| ADR-NNN-{title}.md | File | ADR for significant decisions |
| Confidence metadata | Text | DECOMPOSE→SOLVE→VERIFY→SYNTHESIZE→REFLECT |

---

## Validation Gate
- [ ] Decision table present with D1+ entries
- [ ] Each decision has scope + rationale
- [ ] Firebase services checklist completed
- [ ] Fact-check results documented
- [ ] Confidence ≥ 0.95

---

## 5. Self-Correction Triggers

> [!WARNING]
> IF confidence < 0.95 THEN trigger Socratic debate via iic-clarify + additional WebSearch.

> [!WARNING]
> IF plan references Docker/AWS/Azure THEN **STOP**. Redirect to Firebase equivalent per R-002.

## Usage

Example invocations:

- "/iic-plan-generator" — Run the full iic plan generator workflow
- "iic plan generator on this project" — Apply to current context


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
