---
name: meta-skill-creator
description: Create new 10x skills using the skill-forge protocol. Loads reference sub-repo, applies Trinity (Alfa-Atoms-Beta), validates with 10/10 rubric. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montano
tags: [meta, forge, create, scaffold]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# meta-skill-creator {Meta} (v1.0)

> **"Skills that create, review, search, and deploy other skills."**

## Purpose
Factory for new skills. Follows the skill-forge Trinity: load context (Alfa) → manufacture (Atoms) → verify (Beta). Every skill must score 10/10. [EXPLICIT]

**When to use:** `/jm:create-skill "skill description"`

## Core Principles
1. **Law of Context-First:** Read reference/ before writing. knowledge_graph → best_practices → output_template → self_evaluation. [EXPLICIT]
2. **Law of 10/10:** No skill ships below 10/10 on self-evaluation rubric. [EXPLICIT]
3. **Law of MOAT:** Every skill gets SKILL.md + reference/ + prompts/ + examples/ + tests/. [EXPLICIT]

## Core Process
### Phase 1: Context Loading
1. Read skill-forge reference files (knowledge_graph, best_practices, output_template, self_evaluation). [EXPLICIT]
2. Decompose user request into the knowledge graph taxonomy. [EXPLICIT]

### Phase 2: Manufacture
1. Draft SKILL.md using output_template scaffold. [EXPLICIT]
2. Create reference/ files if skill has >3 laws or >5 steps. [EXPLICIT]
3. Create at least one prompt in prompts/. [EXPLICIT]

### Phase 3: Verify
1. Score against self_evaluation rubric — must achieve 10/10. [EXPLICIT]
2. Run 5 adversarial tests (ambiguity, edge case, contradiction, stress, security). [EXPLICIT]
3. Update skills_index.json via meta-skill-indexer. [EXPLICIT]

## Validation Gate
- [ ] Operation completed successfully
- [ ] skills_index.json updated if needed
- [ ] context.json reflects current state
- [ ] No stack violations (R-002, R-003)

## 4. Self-Correction Triggers
> [!WARNING]
> IF skills_index.json is stale THEN regenerate before searching.
> IF deploying a skill with status != production THEN WARN user.

## Usage

Example invocations:

- "/meta-skill-creator" — Run the full meta skill creator workflow
- "meta skill creator on this project" — Apply to current context


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
