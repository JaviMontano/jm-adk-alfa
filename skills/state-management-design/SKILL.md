---
name: state-management-design
description: Client-side state architecture. Redux/NgRx/Zustand/Context patterns adapted for Firebase real-time listeners and offline persistence. [EXPLICIT]
version: 1.0.0
status: production
owner: Javier Montaño
tags: [architecture, state, redux, ngrx, firebase-realtime]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---
# state-management-design {Architecture} (v1.0)
> **"Firebase is real-time. Your state management must be too."**
## Purpose
Designs client-side state architecture that integrates with Firebase real-time listeners (onSnapshot). Covers React (Redux/Zustand/Context) and Angular (NgRx/Signals) patterns. [EXPLICIT]
**When to use:** Designing state management for React or Angular apps with Firebase.
## Core Principles
1. **Law of Real-Time:** Firestore onSnapshot listeners push state. Don't poll. [EXPLICIT]
2. **Law of Offline:** Enable Firestore offline persistence. State must handle offline/online transitions. [EXPLICIT]
3. **Law of Minimal Store:** Only store in global state what multiple components need. Local state for component-specific data. [EXPLICIT]
## Core Process
### Phase 1: Identify global vs local state needs.
### Phase 2: Select state library (React: Zustand/Redux Toolkit, Angular: NgRx/Signals).
### Phase 3: Design Firestore listener → store sync pattern. Handle loading/error/success states.
## Validation Gate
- [ ] Real-time listeners integrated with state store
- [ ] Offline persistence handled
- [ ] Loading/error states managed
- [ ] No unnecessary global state

## Usage

Example invocations:

- "/state-management-design" — Run the full state management design workflow
- "state management design on this project" — Apply to current context


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
