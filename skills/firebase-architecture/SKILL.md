---
name: firebase-architecture
description: End-to-end Firebase project architecture. Firestore schema strategy, Cloud Functions topology, Hosting config, Security Rules design. C4 diagram output. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, firebase, design, c4]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# firebase-architecture {Architecture} (v1.0)
> **"Firebase is the platform. Architecture is how you use it without hitting walls."**
## Purpose
Designs complete Firebase project architecture covering Firestore data model, Cloud Functions topology, Hosting configuration, Security Rules strategy, and service integration patterns. [EXPLICIT]
**When to use:**
- Starting a new Firebase project
- Redesigning an existing Firebase architecture
- When `/jm:design-architecture` targets Firebase
## Core Principles
1. **Law of Denormalization:** Firestore rewards reading over writing. Model for your queries, not your entities. [EXPLICIT]
2. **Law of Triggers:** Cloud Functions react to events. Design event chains, not request chains. [EXPLICIT]
3. **Law of Rules:** Security Rules are your last line. Design them BEFORE implementation. [EXPLICIT]
## Core Process
### Phase 1: Service Selection
1. Map FR-XXX requirements to Firebase services (Auth, Firestore, Functions, Hosting, Storage). [EXPLICIT]
2. Identify Google Cloud services needed (Cloud Tasks, Pub/Sub, Secret Manager). [EXPLICIT]
3. Identify third-party integrations (Algolia, SendGrid, Stripe). [EXPLICIT]
### Phase 2: Architecture Design
1. Design Firestore collection hierarchy (top-level collections, subcollections, composite indexes). [EXPLICIT]
2. Design Cloud Functions topology (HTTP triggers, Firestore triggers, Auth triggers, scheduled). [EXPLICIT]
3. Design Security Rules strategy (role-based via custom claims, resource-based). [EXPLICIT]
4. Design Hosting config (rewrites for SPA, headers, preview channels). [EXPLICIT]
5. Produce C4 context and container diagrams (Mermaid). [EXPLICIT]
### Phase 3: Document
1. Write architecture document with service matrix. [EXPLICIT]
2. Create ADR for significant decisions. [EXPLICIT]
3. Estimate Firebase costs (reads/writes/invocations). [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| spec.md or requirements | File/Text | Yes | What to build |
| Output | Type | Description |
|--------|------|-------------|
| Architecture document | Markdown | C4 diagrams + service matrix |
| ADR | File | Key decisions |
## Validation Gate
- [ ] All FR-XXX mapped to Firebase services
- [ ] Firestore schema designed for query patterns
- [ ] Security Rules strategy documented
- [ ] C4 diagrams produced (Mermaid)
- [ ] No AWS/Azure references (R-002)
## 5. Self-Correction Triggers
> [!WARNING]
> IF designing SQL-style normalized schema THEN **STOP**. Firestore requires denormalization.
> IF adding Docker/K8s to architecture THEN **STOP**. Use Firebase Hosting + Hostinger (R-003).

## Usage

Example invocations:

- "/firebase-architecture" — Run the full firebase architecture workflow
- "firebase architecture on this project" — Apply to current context


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
