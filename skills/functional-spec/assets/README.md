# Functional Spec Assets

These assets support deterministic functional specification generation.

| Asset | Purpose |
|---|---|
| `functional-spec-template.md` | Required section order for specs. |
| `use-case-schema.json` | Minimum use case fields and count. |
| `business-rule-taxonomy.json` | Stable rule categories. |
| `acceptance-criteria-patterns.json` | Given/When/Then and checklist patterns. |
| `firestore-model-template.json` | Required Firestore collection metadata. |

Use `scripts/compile-functional-spec.py` to turn a structured JSON spec into a validated Markdown specification.
