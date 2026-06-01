# Domain Knowledge — functional spec

## Overview

Functional specification work is a product-analysis artifact, not a technical implementation plan. It answers what the MVP must support, how users move through it, which rules govern behavior, and which data entities must exist for Firebase feasibility. [EXPLICIT]

## Key Concepts

| Concept | Definition | Relevance |
|---|---|---|
| MVP module | Functional area that can be scoped, prioritized, and validated. | Direct input to release planning. [EXPLICIT] |
| Use case | Actor-goal interaction with trigger, preconditions, flow, and acceptance. | Prevents vague feature lists. [EXPLICIT] |
| Business rule | Constraint that must remain true across use cases. | Drives acceptance tests and validation. [EXPLICIT] |
| Firestore model note | Collection-level feasibility note, not implementation code. | Keeps Firebase lens visible without crossing into build plan. [EXPLICIT] |
| Evidence taxonomy | [CODE]/[CONFIG]/[DOC]/[INFERENCE]/[ASSUMPTION]. | Required for factual claims. [EXPLICIT] |

## Best Practices

1. Start with evidence gathering before analysis. [EXPLICIT]
2. Keep implementation details out of the functional spec; defer to architecture and engineering plans. [EXPLICIT]
3. Write at least 8 use cases for an MVP unless the user explicitly scopes a smaller slice. [EXPLICIT]
4. Link business rules to use cases so rules are testable. [EXPLICIT]
5. State open questions and out-of-scope boundaries before handoff. [EXPLICIT]

## Anti-Patterns

| Anti-Pattern | Why It Fails | Better Alternative |
|---|---|---|
| Feature list without actors | Hides user goals and acceptance. | Use actor-goal use cases. |
| Rules without traceability | Rules become unverifiable. | Link each rule to use cases. |
| Acceptance as vague quality | Cannot test completion. | Use Given/When/Then or checklist outcomes. |
| Implementation leakage | Prematurely constrains architecture. | Stop at functional data model notes. |
