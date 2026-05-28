---
name: component-designer
description: UI component architecture. Atomic design (atoms/molecules/organisms). Props contracts. Composition patterns. Accessibility built-in. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, components, atomic-design, a11y]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# component-designer {Architecture} (v1.0)
> **"A component is a contract: props in, UI out, accessible always."**
## Purpose
Designs UI component architecture using atomic design (atoms → molecules → organisms → templates → pages). Defines props contracts, composition patterns, and accessibility requirements. [EXPLICIT]
**When to use:** Designing component libraries or page layouts for React/Angular.
## Core Principles
1. **Law of Atoms:** Start small. Buttons, inputs, labels are atoms. Compose up. [EXPLICIT]
2. **Law of Props:** Every component has a typed props interface. No implicit props. [EXPLICIT]
3. **Law of A11y:** Every interactive component has ARIA attributes, keyboard handling, focus management. [EXPLICIT]
## Core Process
### Phase 1: Identify UI patterns from spec/designs.
### Phase 2: Classify into atomic levels. Define props interfaces.
### Phase 3: Document composition rules and accessibility requirements.
## Validation Gate
- [ ] Components classified by atomic level
- [ ] Props interfaces defined (TypeScript)
- [ ] Accessibility requirements per component
- [ ] Composition patterns documented

## Usage

Example invocations:

- "/component-designer" — Run the full component designer workflow
- "component designer on this project" — Apply to current context


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
