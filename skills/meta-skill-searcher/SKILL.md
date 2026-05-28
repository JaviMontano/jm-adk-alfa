---
name: meta-skill-searcher
description: BM25 search over the skills catalog. Finds relevant skills by keyword, domain, or capability. Uses skills_index.json. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montano
tags: [meta, search, bm25, discovery]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# meta-skill-searcher {Meta} (v1.0)

> **"Skills that create, review, search, and deploy other skills."**

## Purpose
Skill discovery engine. Searches the skills_index.json catalog using BM25 ranking algorithm. [EXPLICIT]

**When to use:** `/jm:search-skill "firebase auth"` or when routing needs skill matching.

## Core Principles
1. **Law of Index:** Always search skills_index.json, never scan directories directly. [EXPLICIT]
2. **Law of Ranking:** BM25 scoring: term frequency, inverse document frequency, document length normalization. [EXPLICIT]
3. **Law of Domain:** Filter by domain: core, analysis, architecture, frontend, backend, data, security, testing, devops, performance, documentation, meta, iic. [EXPLICIT]

## Core Process
### Phase 1: Parse search query + optional domain filter.
### Phase 2: Load skills_index.json, run BM25 ranking.
### Phase 3: Return top 5 results with scores and descriptions.

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

- "/meta-skill-searcher" — Run the full meta skill searcher workflow
- "meta skill searcher on this project" — Apply to current context


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
