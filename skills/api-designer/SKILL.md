---
name: api-designer
description: REST/GraphQL API design for Firebase Cloud Functions. OpenAPI spec generation. Versioning strategy. Rate limiting patterns. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, api, rest, graphql, cloud-functions]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# api-designer {Architecture} (v1.0)
> **"An API is a contract. Design it before you code it."**
## Purpose
Designs REST or GraphQL APIs implemented as Firebase Cloud Functions HTTP triggers. Produces OpenAPI specs, defines versioning, and establishes rate limiting patterns. [EXPLICIT]
**When to use:**
- Designing Cloud Functions HTTP endpoints
- Creating API contracts before implementation
## Core Principles
1. **Law of Contract-First:** OpenAPI/GraphQL schema BEFORE code. No coding without a spec. [EXPLICIT]
2. **Law of Versioning:** URL-based versioning (`/v1/`, `/v2/`). Never break existing consumers. [EXPLICIT]
3. **Law of Functions:** Each endpoint = one Cloud Function. Shared middleware via middleware chain. [EXPLICIT]
## Core Process
### Phase 1: Design
1. Map FR-XXX to endpoints (CRUD operations). [EXPLICIT]
2. Define request/response schemas. [EXPLICIT]
3. Design auth middleware (Firebase ID token verification). [EXPLICIT]
### Phase 2: Document
1. Generate OpenAPI 3.0 spec or GraphQL schema. [EXPLICIT]
2. Define error response format (code, message, details). [EXPLICIT]
3. Document rate limiting strategy. [EXPLICIT]
## 3. Inputs / Outputs
| Input | Type | Required | Description |
|-------|------|----------|-------------|
| spec.md | File | Yes | Requirements |
| Output | Type | Description |
|--------|------|-------------|
| API spec | OpenAPI/GraphQL | Contract document |
## Validation Gate
- [ ] All endpoints have request/response schemas
- [ ] Auth middleware defined
- [ ] Error format standardized
- [ ] Versioning strategy documented
## 5. Self-Correction Triggers
> [!WARNING]
> IF designing endpoints without auth THEN add Firebase ID token verification middleware.

## Usage

Example invocations:

- "/api-designer" — Run the full api designer workflow
- "api designer on this project" — Apply to current context


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
