---
name: auth-architecture
description: Firebase Auth setup. Custom claims for RBAC. Session management. MFA configuration. Provider selection. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, auth, firebase-auth, rbac]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# auth-architecture {Architecture} (v1.0)
> **"Auth is not a feature. It's the foundation."**
## Purpose
Designs authentication and authorization architecture using Firebase Auth. Covers provider selection, custom claims for RBAC, session management, and MFA. [EXPLICIT]
**When to use:** Setting up auth for any Firebase project.
## Core Principles
1. **Law of Claims:** Use custom claims for roles (admin, editor, viewer). Set via Admin SDK. [EXPLICIT]
2. **Law of Rules:** Firestore Security Rules read `request.auth.token` claims for authorization. [EXPLICIT]
3. **Law of Providers:** Start with email/password + Google. Add others as needed. [EXPLICIT]
## Core Process
### Phase 1: Select auth providers based on user requirements.
### Phase 2: Design role hierarchy and custom claims structure.
### Phase 3: Design Security Rules that enforce claims. Configure MFA if required.
## Validation Gate
- [ ] Auth providers selected and documented
- [ ] Custom claims structure defined
- [ ] Security Rules enforce claims
- [ ] Session management strategy documented

## Usage

Example invocations:

- "/auth-architecture" — Run the full auth architecture workflow
- "auth architecture on this project" — Apply to current context


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
