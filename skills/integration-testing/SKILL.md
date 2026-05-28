---
name: integration-testing
description: Firebase Emulator Suite integration tests for Firestore rules, Cloud Functions, and Auth flows
version: 1.0.0
status: production
owner: Javier Montaño
tags: [testing, integration, firebase-emulator, firestore-rules, cloud-functions, auth]
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
---

# 080 — Integration Testing {Testing}

## Purpose
Validate cross-service interactions using Firebase Emulator Suite. Test Firestore security rules, Cloud Functions triggers, and Auth flows against real emulated backends — not mocks. [EXPLICIT]

## Physics — 3 Immutable Laws

1. **Law of Real Contracts**: Integration tests use actual Firebase Emulator instances. No mocking Firestore or Auth at this layer — the emulator IS the contract. [EXPLICIT]
2. **Law of Clean State**: Each test file starts with a fresh emulator state. `clearFirestore()` and `clearAuth()` run in `beforeEach`. [EXPLICIT]
3. **Law of Boundary Testing**: Integration tests validate the seams — service-to-service, rule enforcement, trigger chains. Internal logic belongs in unit tests. [EXPLICIT]

## Protocol

### Phase 1 — Emulator Bootstrap
1. Ensure `firebase.json` has emulator config (see skill 087). [EXPLICIT]
2. Install `@firebase/rules-unit-testing` for Firestore rules tests. [EXPLICIT]
3. Create `test/integration/` directory with setup file that connects to emulator ports. [EXPLICIT]
4. Script: `firebase emulators:exec --only firestore,auth,functions "vitest run --config vitest.integration.config.ts"`. [EXPLICIT]

### Phase 2 — Test Authoring
1. **Firestore Rules**: Test allow/deny for each collection with authenticated/unauthenticated contexts. [EXPLICIT]
2. **Cloud Functions**: Trigger `onCreate`, `onUpdate`, `onDelete` via emulator writes. Assert side effects. [EXPLICIT]
3. **Auth Flows**: Create test users via Auth emulator. Validate custom claims propagation. [EXPLICIT]

### Phase 3 — Assertion & Reporting
1. Assert Firestore document states after function triggers complete. [EXPLICIT]
2. Validate security rule denials throw `permission-denied`. [EXPLICIT]
3. Export emulator coverage report: `http://localhost:8080/emulator/v1/projects/{id}:ruleCoverage`. [EXPLICIT]

## I/O

| Input | Output |
|-------|--------|
| Firestore security rules (`firestore.rules`) | Rule coverage report (HTML) |
| Cloud Functions source | Trigger execution logs + assertion results |
| Auth flow definitions | User creation/deletion verification |
| `firebase.json` emulator config | Emulator boot + test execution |

## Quality Gates — 5 Checks

1. **100% Firestore rule coverage** — every rule path has allow AND deny test. [EXPLICIT]
2. **Function triggers tested** — every `onCreate/onUpdate/onDelete` has integration test. [EXPLICIT]
3. **Auth flows verified** — sign-up, sign-in, custom claims, token refresh tested. [EXPLICIT]
4. **Emulator cleanup confirmed** — no state leaks between test files. [EXPLICIT]
5. **CI execution** — `firebase emulators:exec` runs in pipeline with Java 11+. [EXPLICIT]

## Edge Cases

- **Eventual consistency**: Cloud Function triggers are async — use polling or `waitForExpect`.
- **Batch writes in rules**: Test that batched writes fail atomically when one rule denies.
- **Custom claims timing**: Claims update requires token refresh — test with `getIdTokenResult(true)`.
- **Emulator port conflicts**: Use non-default ports in CI to avoid clashes.

## Self-Correction Triggers

- Firestore rule coverage below 100% → block deploy until all paths tested.
- Function trigger test missing → lint rule flags untested exports.
- Emulator fails to start → check Java version, port availability, `firebase.json` config.
- Test pollution detected (order-dependent failures) → enforce `beforeEach` cleanup.

## Usage

Example invocations:

- "/integration-testing" — Run the full integration testing workflow
- "integration testing on this project" — Apply to current context


## Assumptions & Limits

- Assumes access to project artifacts (code, docs, configs) [EXPLICIT]
- Requires English-language output unless otherwise specified [EXPLICIT]
- Does not replace domain expert judgment for final decisions [EXPLICIT]
