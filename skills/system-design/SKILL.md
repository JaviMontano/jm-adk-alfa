---
name: system-design
description: End-to-end system design. Frontend + Firebase backend + Google APIs + third-party integrations. Sequence diagrams. Deployment topology. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, system-design, end-to-end, integration]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# system-design {Architecture} (v1.0)
> **"The system is the sum of its integrations."**
## Purpose
Produces end-to-end system design combining frontend (React/Angular/HTML), Firebase backend, Google APIs, and third-party services into a coherent architecture. [EXPLICIT]
**When to use:** When the project involves multiple services and integrations.
## Core Principles
1. **Law of Boundaries:** Each service has clear boundaries (frontend, backend, database, external). [EXPLICIT]
2. **Law of Contracts:** Service-to-service communication via defined contracts (API specs, event schemas). [EXPLICIT]
3. **Law of Failure:** Design for failure. Every external call needs error handling and fallback. [EXPLICIT]
## Core Process
### Phase 1: Map all system components (frontend, Firebase services, Google APIs, third-party).
### Phase 2: Design interaction patterns (sync API calls, async events, real-time listeners).
### Phase 3: Produce sequence diagrams (Mermaid) for key flows. Document deployment topology.
## Validation Gate
- [ ] All components identified and bounded
- [ ] Interaction patterns documented
- [ ] Sequence diagrams for key flows
- [ ] Error handling for all external calls

## Usage

Example invocations:

- "/system-design" — Run the full system design workflow
- "system design on this project" — Apply to current context


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
