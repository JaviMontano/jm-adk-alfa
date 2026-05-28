---
name: context-optimizer
description: Manages token budget across sessions. Implements lazy loading, context compression, and progressive disclosure to maximize effective context usage. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [core, context, optimization, token-budget]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# context-optimizer {Core} (v1.0)

> **"Load what you need, when you need it. Never the whole library."**

## Purpose

Prevents context window saturation by managing what gets loaded and when. Implements lazy loading of skill references, progressive disclosure of large artifacts, and context compression for long sessions. [EXPLICIT]

**When to use:**

- Automatically during skill loading (implicit)
- When session approaches context limits
- When `/jm:optimize-ctx` is invoked

---

## Core Principles (Immutable Laws)

1. **Law of Lazy Loading:** Never load a skill's full reference/ until the skill is actively executing. [EXPLICIT]
2. **Law of Compression:** Summaries first, details on demand. Show the index, not the book. [EXPLICIT]
3. **Law of Eviction:** Completed phase artifacts can be summarized to free context for active work. [EXPLICIT]

---

## Core Process (Step-by-Step)

### Phase 1: Budget Assessment

1. **Estimate current context usage** (messages, loaded files, skill references). [EXPLICIT]
2. **Identify candidates for eviction** — completed phases, resolved clarifications. [EXPLICIT]
3. **Prioritize active work** — current phase gets full context, others get summaries. [EXPLICIT]

### Phase 2: Optimization Actions

1. **Compress completed artifacts:** Replace full analysis with 5-line summary. [EXPLICIT]
2. **Defer reference loading:** Load skill SKILL.md first; load reference/ only when protocol demands it. [EXPLICIT]
3. **Index-first pattern:** Show skill catalog index before loading individual skills. [EXPLICIT]

---

## 3. Inputs / Outputs

### Inputs

| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Current context | State | Yes | Active session state |
| Active phase | Enum | Yes | Current pipeline phase |

### Outputs

| Output | Type | Description |
|--------|------|-------------|
| Optimized context | State | Compressed session state |
| Eviction report | Text | What was compressed and why |

---

## Validation Gate (10x Checklist)

- [ ] **Active phase** has full context loaded
- [ ] **Completed phases** are summarized (not deleted)
- [ ] **No skill reference** loaded before its skill is active
- [ ] **Index available** for skill discovery without full loading

---

## 5. Self-Correction Triggers

> [!WARNING]
> IF loading a reference/ file that isn't for the active skill THEN **DEFER**. Load only when the skill executes.

## Usage

Example invocations:

- "/context-optimizer" — Run the full context optimizer workflow
- "context optimizer on this project" — Apply to current context


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
