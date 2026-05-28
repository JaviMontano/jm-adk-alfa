---
name: role-based-access
description: RBAC via custom claims. Admin SDK setCustomUserClaims. Firestore rules request.auth.token. Role hierarchy design. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [security, rbac, custom-claims, authorization]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# role-based-access {Security} (v1.0)
> **"Security is not a feature. It's every feature's foundation."**
## Purpose
RBAC via custom claims. Admin SDK setCustomUserClaims. Firestore rules request.auth.token. Role hierarchy design. [EXPLICIT]
**When to use:** Implementing authentication, authorization, or security measures in Firebase projects.
## Core Principles
1. **Law of Auth First:** No endpoint without authentication. Firebase ID token verification is mandatory. [EXPLICIT]
2. **Law of Least Privilege:** Users get minimum permissions needed. Custom claims define roles. [EXPLICIT]
3. **Law of Defense in Depth:** Client validation + Security Rules + Cloud Functions validation. Three layers. [EXPLICIT]
## Core Process
### Phase 1: Assess security requirements from spec.
### Phase 2: Implement auth, authorization, and security measures.
### Phase 3: Audit with OWASP checklist. Test rules with emulator.
## Validation Gate
- [ ] Auth implemented on all endpoints
- [ ] Security rules cover all Firestore collections
- [ ] OWASP Top 10 mitigations addressed
- [ ] Secrets in Secret Manager (not in code)
- [ ] Privacy compliance documented

## Usage

Example invocations:

- "/role-based-access" — Run the full role based access workflow
- "role based access on this project" — Apply to current context


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
