---
name: responsive-design-system
description: Design token system. CSS custom properties, breakpoints, grid, typography scale, theming. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, design-system, tokens, responsive]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# responsive-design-system {Architecture} (v1.0)
> **"Architecture is decisions. Document every one."**
## Purpose
Design token system. CSS custom properties, breakpoints, grid, typography scale, theming. [EXPLICIT]
**When to use:** When designing or reviewing architecture for Firebase/Google stack projects.
## Core Principles
1. **Law of Firebase-First:** All architecture decisions constrained to Firebase/Google ecosystem (R-002). [EXPLICIT]
2. **Law of Evidence:** Every architectural claim tagged [CODE], [CONFIG], [DOC], [INFERENCE], or [ASSUMPTION]. [EXPLICIT]
3. **Law of Diagrams:** Architecture without diagrams is incomplete. Use Mermaid for C4, sequence, flow. [EXPLICIT]
## Core Process
### Phase 1: Analyze requirements and constraints.
### Phase 2: Design architecture with Firebase/Google services.
### Phase 3: Document with C4 diagrams, decision records, and evidence tags.
## Validation Gate
- [ ] Architecture designed within Firebase/Google/Hostinger constraints
- [ ] C4 or sequence diagrams produced (Mermaid)
- [ ] Evidence tags on all claims
- [ ] ADR created for significant decisions
- [ ] No AWS/Azure/Docker references

## Usage

Example invocations:

- "/responsive-design-system" — Run the full responsive design system workflow
- "responsive design system on this project" — Apply to current context


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
