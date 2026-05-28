---
name: server-middleware
description: Auth verification (verifyIdToken), rate limiting, CORS config, request logging, input sanitization middleware. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [backend, middleware, auth, cors, rate-limiting]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# server-middleware {Backend} (v1.0)
> **"Firebase Functions are your backend. Design them like microservices, deploy them like magic."**
## Purpose
Auth verification (verifyIdToken), rate limiting, CORS config, request logging, input sanitization middleware. [EXPLICIT]
**When to use:** Backend development within Firebase/Google ecosystem.
## Core Principles
1. **Law of Functions:** Each Cloud Function does ONE thing. Single responsibility. [EXPLICIT]
2. **Law of Cold Start:** Minimize dependencies. Use lazy imports. Set min instances for critical functions. [EXPLICIT]
3. **Law of Security:** Every HTTP function verifies Firebase ID tokens. No public endpoints without auth. [EXPLICIT]
## Core Process
### Phase 1: Design
1. Map requirements to Cloud Functions triggers (HTTP, Firestore, Auth, Storage, scheduled). [EXPLICIT]
2. Define input/output contracts for each function. [EXPLICIT]
3. Design error handling and retry strategy. [EXPLICIT]
### Phase 2: Implement
1. Create function with proper trigger type. [EXPLICIT]
2. Add auth middleware for HTTP functions. [EXPLICIT]
3. Implement business logic with error handling. [EXPLICIT]
4. Add Cloud Logging for observability. [EXPLICIT]
### Phase 3: Test + Deploy
1. Test with Firebase Emulator Suite. [EXPLICIT]
2. Deploy with `firebase deploy --only functions`. [EXPLICIT]
3. Verify in Firebase Console. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| Requirements | Text/Spec | Yes | What the function does |
| Output | Type | Description |
|--------|------|-------------|
| Cloud Function code | TypeScript | Deployable function |
## Validation Gate
- [ ] Single responsibility per function
- [ ] Auth middleware on HTTP endpoints
- [ ] Error handling with Cloud Logging
- [ ] Emulator tests pass
- [ ] No AWS/Azure services (R-002)
## 5. Self-Correction Triggers
> [!WARNING]
> IF function has no auth middleware THEN add verifyIdToken check.
> IF function imports 10+ dependencies THEN split or lazy-load to reduce cold start.

## Usage

Example invocations:

- "/server-middleware" — Run the full server middleware workflow
- "server middleware on this project" — Apply to current context


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
