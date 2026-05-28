---
name: iic-clarify
description: Socratic debate for ambiguity reduction. Auto-detects artifact, applies question taxonomy, records answers with traceability to FR/US/T IDs. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, socratic, clarification]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-clarify {Metacognition} (v1.0)

> **"The right question prevents 100 wrong assumptions."**

## Purpose
Reduces ambiguity through targeted Socratic questioning. Auto-detects the most recent artifact, applies artifact-specific question taxonomies, and records answers with full traceability. [EXPLICIT]

**When to use:**
- When spec quality score < 6
- When confidence < 0.95 during planning
- When iic-artifact-analyzer detects ambiguity or underspecification
- Anytime understanding is uncertain

---

## Core Principles
1. **Law of Materiality:** Questions MUST materially impact downstream phases. No trivial questions. [EXPLICIT]
2. **Law of Taxonomy:** Each artifact type has specific question categories (spec → scope/priority/edge cases, plan → feasibility/alternatives, tasks → dependencies/effort). [EXPLICIT]
3. **Law of Recording:** Answers recorded in `## Clarifications` section with affected item IDs. [EXPLICIT]

## Core Process
### Phase 1: Detect Artifact
1. Auto-detect most recent artifact: spec, plan, tasks, or constitution. [EXPLICIT]
2. Load artifact-specific question taxonomy. [EXPLICIT]

### Phase 2: Generate Questions
1. Scan artifact for ambiguity triggers (vague terms, missing criteria, unresolved references). [EXPLICIT]
2. Generate 3-7 targeted questions per ambiguity. [EXPLICIT]
3. Rank by impact on downstream phases. [EXPLICIT]

### Phase 3: Record Answers
1. Add `## Clarifications` section to artifact. [EXPLICIT]
2. Format: `- **Q:** {question} → **A:** {answer} | Affects: FR-001, T005`
3. Update affected items with clarification results. [EXPLICIT]

---

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Target artifact | File | Yes | Spec, plan, tasks, or constitution |

| Output | Type | Description |
|--------|------|-------------|
| Clarification questions | Text | Targeted questions |
| Updated artifact | File | Clarifications section added |

## Validation Gate
- [ ] Questions are material (impact downstream phases)
- [ ] Answers linked to affected item IDs
- [ ] Clarifications section added to artifact
- [ ] No questions about information already in artifacts

## 5. Self-Correction Triggers
> [!WARNING]
> IF question answer is already in the artifact THEN **DROP** the question. Don't ask what's documented.

> [!WARNING]
> IF asking more than 10 questions THEN prioritize top 5 by downstream impact.

## Usage

Example invocations:

- "/iic-clarify" — Run the full iic clarify workflow
- "iic clarify on this project" — Apply to current context


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
