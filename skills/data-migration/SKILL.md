---
name: data-migration
description: CSV/JSON import to Firestore. Batch writes (500/batch). Schema evolution. Rollback procedures. Data transformation scripts. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [data, migration, import, batch, evolution]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# data-migration {Data} (v1.0)
> **"Data is the product. Model it for queries, secure it with rules, back it up daily."**
## Purpose
CSV/JSON import to Firestore. Batch writes (500/batch). Schema evolution. Rollback procedures. Data transformation scripts. [EXPLICIT]
**When to use:** Database design, data management, or analytics within Firebase ecosystem.
## Core Principles
1. **Law of Queries:** Design schema for read patterns. Firestore charges per read/write. [EXPLICIT]
2. **Law of Rules:** Security rules are mandatory. No collection without rules. [EXPLICIT]
3. **Law of Backups:** Production data gets scheduled backups. No exceptions. [EXPLICIT]
## Core Process
### Phase 1: Design data model from requirements.
### Phase 2: Implement with security rules and indexes.
### Phase 3: Test with emulator. Validate rules. Set up backups.
## Validation Gate
- [ ] Schema designed for actual query patterns
- [ ] Security rules cover all collections
- [ ] Indexes defined for compound queries
- [ ] Backup strategy documented
- [ ] No SQL-style normalized design in Firestore

## Usage

Example invocations:

- "/data-migration" — Run the full data migration workflow
- "data migration on this project" — Apply to current context


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
