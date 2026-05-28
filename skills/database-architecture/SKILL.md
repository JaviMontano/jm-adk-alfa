---
name: database-architecture
description: Firestore document/collection modeling. Denormalization strategies. Composite indexes. Query optimization. Collection group queries. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, database, firestore, modeling]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# database-architecture {Architecture} (v1.0)
> **"Model for your queries, not your entities."**
## Purpose
Designs Firestore data models optimized for read patterns. Covers document/collection hierarchy, denormalization, composite indexes, and query optimization. [EXPLICIT]
**When to use:** Designing or refactoring Firestore schema.
## Core Principles
1. **Law of Reads:** Optimize for reads. Duplicate data to avoid joins. [EXPLICIT]
2. **Law of 1MB:** Documents max 1MB. If growing unbounded, use subcollections. [EXPLICIT]
3. **Law of Indexes:** Composite indexes for multi-field queries. Plan before writing. [EXPLICIT]
## Core Process
### Phase 1: Identify query patterns from FR-XXX.
### Phase 2: Design collections, documents, subcollections. Define indexes.
### Phase 3: Document schema with example documents.
## Validation Gate
- [ ] Schema designed for actual query patterns
- [ ] No unbounded arrays in documents
- [ ] Composite indexes defined
- [ ] Security rules considered in schema design

## Usage

Example invocations:

- "/database-architecture" — Run the full database architecture workflow
- "database architecture on this project" — Apply to current context


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
