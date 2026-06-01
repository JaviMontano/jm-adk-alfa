# Functional Spec — Body of Knowledge

## Canon

A functional specification defines what the product must do before architecture or implementation begins. For this kit, a complete spec includes MVP modules, at least 8 use cases, typed business rules, acceptance criteria, Firestore data model notes, explicit out-of-scope boundaries, open questions, and an evidence summary.

## Required Sections

| Section | Purpose | Deterministic Check |
|---|---|---|
| MVP Modules | Decompose the product into buildable functional areas. | Non-empty `mvp_modules`. |
| Use Cases | Describe actor goals and behavior. | At least 8 entries matching `UC-###`. |
| Business Rules | Capture validation, workflow, authorization, notification, retention, billing, and audit constraints. | Rules match taxonomy and link to known use cases. |
| Acceptance Criteria | Convert use cases into testable outcomes. | Every use case has at least one criterion. |
| Firestore Data Model | Confirm Firebase feasibility without designing implementation internals. | Collections declare owner, PII, fields, indexes, retention. |

## Asset Usage

- `assets/functional-spec-template.md`: canonical section order.
- `assets/use-case-schema.json`: minimum fields and count.
- `assets/business-rule-taxonomy.json`: allowed rule types and traceability fields.
- `assets/acceptance-criteria-patterns.json`: accepted criterion formats.
- `assets/firestore-model-template.json`: collection metadata requirements.

## Scripted Spec

Use `scripts/compile-functional-spec.py --spec <spec.json>` when requirements can be represented as JSON. The compiler rejects incomplete specs, so it is useful for preventing probabilistic omissions in repeated specification work.

## Quality Metrics

| Metric | Target | How to Measure |
|--------|--------|---|
| Use case coverage | >= 8 | `compile-functional-spec.py` validation. |
| Business rule traceability | 100% | Every rule links to known use cases. |
| Acceptance coverage | 100% | Every use case has at least one acceptance criterion. |
| Firestore feasibility | 100% | Collections include owner, PII, fields, indexes, retention. |
