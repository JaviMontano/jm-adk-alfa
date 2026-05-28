---
name: iic-implement
description: Red-green-verify implementation cycle. Verifies hash integrity of .feature files. NEVER modifies test assertions. Enforces coverage. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [metacognition, integrity, implementation, tdd]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# iic-implement {Metacognition} (v1.0)

> **"Tests are sacred. Code bends to tests, never the reverse."**

## Purpose
Guides implementation following red-green-verify TDD cycle. Verifies SHA256 hash integrity of .feature files before coding. Blocks any attempt to modify test assertions. [EXPLICIT]

**When to use:**
- After tasks.md is approved (post-G2)
- During active development phase

---

## Core Principles
1. **Law of Hash Integrity:** Before coding, verify .feature file hashes match context.json. Mismatch = STOP. [EXPLICIT]
2. **Law of Red-Green:** Write code to pass existing tests. NEVER modify tests to match code. [EXPLICIT]
3. **Law of Coverage:** 100% of .feature scenarios must have passing step implementations. [EXPLICIT]

## Core Process
### Phase 1: Pre-Implementation
1. Verify .feature hash integrity against context.json. [EXPLICIT]
2. Read tasks.md for current task [T###]. [EXPLICIT]
3. Confirm task has US-X link and corresponding .feature scenarios. [EXPLICIT]

### Phase 2: Red-Green-Verify
1. **RED:** Run tests — confirm they fail (expected). [EXPLICIT]
2. **GREEN:** Write minimal code to pass tests. [EXPLICIT]
3. **VERIFY:** Run full test suite — all green. [EXPLICIT]
4. Repeat for next task. [EXPLICIT]

### Phase 3: Progress Update
1. Update context.json stage: `implementing-NN%`. [EXPLICIT]
2. Mark completed tasks in tasks.md: `- [x] [T###]`. [EXPLICIT]

## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| tasks.md | File | Yes | Task to implement |
| *.feature files | Gherkin | Yes | Hash-locked tests |
| context.json | JSON | Yes | Hash verification |

| Output | Type | Description |
|--------|------|-------------|
| Source code | Files | Implementation |
| context.json update | JSON | Progress percentage |

## Validation Gate
- [ ] Hash integrity verified before coding
- [ ] No .feature files modified
- [ ] All tests pass after implementation
- [ ] Coverage 100% of scenarios
- [ ] context.json progress updated

## 5. Self-Correction Triggers
> [!WARNING]
> IF .feature hash mismatch THEN **STOP**. Do not code. Report integrity violation.

> [!WARNING]
> IF test modified to pass THEN **REVERT**. Fix code, not tests.

## Usage

Example invocations:

- "/iic-implement" — Run the full iic implement workflow
- "iic implement on this project" — Apply to current context


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
