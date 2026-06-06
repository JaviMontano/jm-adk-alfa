# Guardrails Management — Body of Knowledge

## Canon
- Guardrails are durable only after explicit user confirmation. [DOC]
- Rules must be specific, scoped, source-backed, and enforceable by a future
  Guardian. [DOC]
- A proposed rule is not a stored rule until the confirmation packet says
  `status: confirmed`. [DOC]
- Duplicate and conflict checks run across guidelines, constraints, and
  guardrails before any write. [DOC]
- Removal preserves audit history by setting `active: false`; it does not delete
  the entry. [DOC]

## Canonical Rule Fields

| Field | Purpose |
|-------|---------|
| `id` | Stable ID using `GL-`, `CT-`, or `GR-` prefix |
| `type` | `guideline`, `constraint`, or `guardrail` |
| `rule` | Durable working rule text |
| `scope` | Where the rule applies |
| `source` | `user-explicit`, `user-confirmed`, or `system-import` |
| `confirmed_date` | ISO date from the operation packet |
| `active` | Boolean enforcement state |
| `evidence_tag` | `[CONFIG]`, `[DOC]`, `[CÓDIGO]`, `[INFERENCIA]`, or `[SUPUESTO]` |
| `verifiable_check` | How Guardian can test compliance |
| `target_file` | Canonical JSON file for this type |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Confirmation coverage | 100% | Stored entries have explicit confirmation |
| Schema validity | 100% | Entries satisfy `assets/rule-schema.json` |
| Classification accuracy | 100% | Type, ID prefix, and target file agree |
| Duplicate safety | 100% | Normalized active duplicate rules are blocked |
| Enforcement readiness | 100% | Every active rule has a verifiable check |

## Anti-Patterns

- Saving "make outputs better" without a measurable check. [DOC]
- Treating "maybe we should" as confirmation. [DOC]
- Writing constraints into `guidelines.json`. [DOC]
- Deleting a rule instead of deactivating it. [DOC]

## References
- `assets/rule-schema.json`
- `assets/classification-policy.json`
- `assets/confirmation-policy.json`
- `assets/conflict-policy.json`
- `assets/storage-map.json`
- `assets/report-contract.json`
