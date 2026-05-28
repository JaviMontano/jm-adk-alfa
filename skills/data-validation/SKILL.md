---
name: data-validation
description: Client-side Zod/Yup schemas. Server-side Cloud Functions validation. Firestore rules validation. End-to-end type safety. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [data, validation, zod, type-safety]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# data-validation {Data} (v1.0)
> **"Data is the product. Model it for queries, secure it with rules, back it up daily."**
## Purpose
Client-side Zod/Yup schemas. Server-side Cloud Functions validation. Firestore rules validation. End-to-end type safety. [EXPLICIT]
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

- "/data-validation" — Run the full data validation workflow
- "data validation on this project" — Apply to current context


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
