<!--
generated-by: scripts/scaffold-skill.py
generated-for: functional-spec
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

The Field Service MVP functional specification includes four MVP modules, eight actor-goal use cases, four typed business rules, acceptance criteria for every use case, Firestore feasibility notes, explicit out-of-scope boundaries, and open questions.

## Deterministic Spec

- Run: `python3 skills/functional-spec/scripts/compile-functional-spec.py --spec skills/functional-spec/scripts/fixtures/mvp-spec.json`
- Output sections: Evidence Summary, MVP Modules, Use Cases, Business Rules, Acceptance Criteria, Firestore Data Model, Out of Scope, Open Questions.

## Functional Controls

- `UC-001` through `UC-008` preserve actor, trigger, preconditions, main flow, and acceptance.
- `BR-001` through `BR-004` link validation, workflow, authorization, and notification rules to concrete use cases.
- Firestore notes include `serviceRequests` and `workOrders` collections with owner, PII, indexes, and retention.

## Validation

- `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill functional-spec`
- `python3 -B scripts/validate-skill-dod.py --skill functional-spec`
