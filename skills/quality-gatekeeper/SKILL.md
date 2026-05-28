---
name: quality-gatekeeper
description: Validates deliverables at quality gates G0-G3. Blocks phase transitions until criteria are met. Produces pass/fail reports with evidence. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [core, quality, gates, validation]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# quality-gatekeeper {Core} (v1.0)

> **"No gate, no advance. No evidence, no pass."**

## Purpose

Enforces the 4 quality gates (G0-G3) that govern phase transitions in the JM-ADK pipeline. Validates that deliverables meet defined criteria before allowing advancement. [EXPLICIT]

**When to use:**

- Before transitioning between pipeline phases
- When `/jm:advance` is invoked
- When manually checking gate readiness

---

## Core Principles (Immutable Laws)

1. **Law of Gates:** G0 (pre-flight) → G1 (analysis) → G2 (architecture) → G3 (deploy). No skipping. [EXPLICIT]
2. **Law of Evidence:** Every pass requires tagged evidence `[CODE]`/`[CONFIG]`/`[DOC]`. No evidence = no pass. [EXPLICIT]
3. **Law of Blocking:** A failed gate BLOCKS all downstream work. Fix → re-evaluate → pass. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Gate Identification

1. **Determine current phase** from `.specify/context.json` stage field. [EXPLICIT]
2. **Select gate criteria** from the gate table below. [EXPLICIT]

### Phase 2: Evaluation

| Gate | Criteria | Pass Condition |
|------|----------|---------------|
| G0 | Secrets scan, stack compliance (R-002/R-003) | Zero violations |
| G1 | Analysis deliverables complete, evidence tags present, stakeholder map exists | All artifacts exist with evidence |
| G2 | Firebase architecture documented, data model validated, security rules drafted | Architecture review passed |
| G3 | Tests pass, Lighthouse > 90, security audit clean, monitoring configured | All checks green |

1. **Run checks** for each criterion. [EXPLICIT]
2. **Tag results** with evidence source. [EXPLICIT]
3. **Score:** Pass (all criteria met) or Fail (list failures). [EXPLICIT]

### Phase 3: Report

1. **Produce gate report** with pass/fail per criterion. [EXPLICIT]
2. **Update** `.specify/score-history.json` with findings. [EXPLICIT]
3. **If pass:** Allow phase transition. [EXPLICIT]
4. **If fail:** Block advancement, list remediation steps. [EXPLICIT]

---

## 3. Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Gate ID | Enum | Yes | G0, G1, G2, or G3 |
| Artifacts | Files | Yes | Deliverables to evaluate |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| Gate Report | Markdown | Pass/fail per criterion with evidence |
| Score Update | JSON | Updated score-history.json entry |

---

## Validation Gate (10x Checklist)

- [ ] **Gate identified** correctly from context
- [ ] **All criteria evaluated** with evidence tags
- [ ] **Score updated** in score-history.json
- [ ] **Remediation steps** listed for any failures
- [ ] **Advancement blocked** if any criterion fails

---

## 5. Edge Cases & Antipatterns

### Antipatterns

- **Rubber-stamping:** Passing a gate without checking criteria → **BAD**
- **Partial pass:** "Most criteria met, let's proceed" → **BAD**. All must pass.

### Edge Cases

- **G0 on empty project:** Still requires stack compliance check (no AWS/Azure in CLAUDE.md).
- **Re-evaluation:** After fixing failures, re-run the gate — don't assume it passes.

---

## 6. Self-Correction Triggers

> [!WARNING]
> IF gate evaluation finds >30% `[ASSUMPTION]` tags THEN add WARNING banner to gate report.

> [!WARNING]
> IF G3 is requested but G1 hasn't passed THEN **STOP**. Gates are sequential.

## Usage

Example invocations:

- "/quality-gatekeeper" — Run the full quality gatekeeper workflow
- "quality gatekeeper on this project" — Apply to current context


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
