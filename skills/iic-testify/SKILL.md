---
name: iic-testify
description: Generates Gherkin .feature files from spec.md. SHA256 hash-locks assertions BEFORE implementation. Prevents silent requirement drift. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, testing, bdd]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-testify {Metacognition} (v1.0)

> **"Tests are written from specs, not from code. Hash-locked, immutable until re-specified."**

## Purpose
Transforms spec.md requirements into Gherkin .feature files. Computes SHA256 hashes for each feature file and stores them in context.json. These hashes LOCK assertions before implementation begins. [EXPLICIT]

**When to use:**
- After spec.md is approved
- Before implementation starts
- When TDD flag is true in context.json

---

## Core Principles
1. **Law of Spec-First:** .feature files generated from spec.md FR-XXX/US-X/SC-XXX. NEVER from code. [EXPLICIT]
2. **Law of Hash-Lock:** SHA256 hash computed and stored in context.json BEFORE implementation. [EXPLICIT]
3. **Law of Immutability:** Modifying .feature files during implementation is BLOCKED. Change spec → re-testify → re-hash. [EXPLICIT]

## Core Process
### Phase 1: Parse Spec
1. Extract FR-XXX, US-X, SC-XXX from spec.md. [EXPLICIT]
2. Map each to Gherkin scenarios (Given/When/Then). [EXPLICIT]

### Phase 2: Generate Features
1. Write `specs/{feature}/tests/features/*.feature` files. [EXPLICIT]
2. Tag with `@FR-001`, `@US-1`, `@SC-001`. [EXPLICIT]
3. Include `# DO NOT MODIFY — hash-locked` header. [EXPLICIT]

### Phase 3: Hash-Lock
1. Compute SHA256 for each .feature file. [EXPLICIT]
2. Store in `.specify/context.json` assertions object. [EXPLICIT]
3. Format: `{ "file": "hash" }`

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| spec.md | File | Yes | Source requirements |

| Output | Type | Description |
|--------|------|-------------|
| *.feature files | Gherkin | Hash-locked test scenarios |
| context.json update | JSON | SHA256 hashes stored |

## Validation Gate
- [ ] Every FR-XXX has at least one scenario
- [ ] All features tagged with spec IDs
- [ ] SHA256 hashes stored in context.json
- [ ] DO NOT MODIFY header present
- [ ] No implementation details in feature files

## 5. Self-Correction Triggers
> [!WARNING]
> IF .feature file modified during implementation THEN **BLOCK**. Re-specify first.

## Usage

Example invocations:

- "/iic-testify" — Run the full iic testify workflow
- "iic testify on this project" — Apply to current context


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
