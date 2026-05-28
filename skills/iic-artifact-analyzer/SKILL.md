---
name: iic-artifact-analyzer
description: Non-destructive cross-artifact consistency analysis. 8 detection categories. Health score 0-100. Updates score-history.json. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, analysis, health]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-artifact-analyzer {Metacognition} (v1.0)

> **"I read everything. I change nothing. I report what I find."**

## Purpose
Cross-artifact consistency checks across spec, plan, tasks, tests, and constitution. Produces analysis.md report with findings across 8 categories. Computes health score (0-100). [EXPLICIT]

**When to use:**
- Before any quality gate evaluation
- After significant artifact changes
- When `/jm:audit` is invoked

---

## Core Principles
1. **Law of Non-Destruction:** Read-only analysis. NEVER modify artifacts. [EXPLICIT]
2. **Law of 8 Categories:** Check duplication, ambiguity, underspecification, constitution alignment, phase violations, coverage gaps, inconsistency, prose quality. [EXPLICIT]
3. **Law of Scoring:** `score = 100 - (critical*20 + high*5 + medium*2 + low*0.5)`, floored at 0. [EXPLICIT]

## Core Process
### Phase 1: Load Artifacts
1. Read all artifacts: CONSTITUTION.md, spec.md, plan-*.md, tasks.md, *.feature files. [EXPLICIT]

### Phase 2: Analyze
1. **Duplication:** Same requirement in multiple places. [EXPLICIT]
2. **Ambiguity:** Vague terms without measurable criteria. [EXPLICIT]
3. **Underspecification:** FR-XXX without acceptance criteria. [EXPLICIT]
4. **Constitution alignment:** Art. 1.4 (stack), Art. 1.5 (phase separation). [EXPLICIT]
5. **Phase violations:** Implementation in spec, governance in plan. [EXPLICIT]
6. **Coverage gaps:** FR-XXX without test scenario. [EXPLICIT]
7. **Inconsistency:** Contradictions between artifacts. [EXPLICIT]
8. **Prose quality:** Fluff words (R-008 violations). [EXPLICIT]

### Phase 3: Score + Report
1. Classify findings: CRITICAL, HIGH, MEDIUM, LOW. [EXPLICIT]
2. Compute health score. [EXPLICIT]
3. Update `.specify/score-history.json`. [EXPLICIT]
4. Produce analysis.md. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| All project artifacts | Files | Yes | Spec, plan, tasks, tests, constitution |

| Output | Type | Description |
|--------|------|-------------|
| analysis.md | File | Findings report |
| score-history.json update | JSON | Timestamped score entry |

## Validation Gate
- [ ] All 8 categories checked
- [ ] Findings classified by severity
- [ ] Health score computed correctly
- [ ] score-history.json updated
- [ ] No artifacts modified (read-only)

## Usage

Example invocations:

- "/iic-artifact-analyzer" — Run the full iic artifact analyzer workflow
- "iic artifact analyzer on this project" — Apply to current context


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
