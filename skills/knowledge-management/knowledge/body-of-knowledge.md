# Knowledge Management — Body of Knowledge

## Canon
- Knowledge is usable only when it has provenance, owner, retrieval metadata,
  freshness policy, and a next action. [DOC]
- Claims without source paths remain gaps until verified. [DOC]
- Decay review must use an explicit `reference_date` and stored source dates,
  never the runtime clock. [DOC]
- Searchability requires at least one path, one owner, and enough keywords for a
  future operator to retrieve the item without conversational memory. [DOC]
- Duplicate or contradictory sources must be resolved by priority, timestamp, or
  explicit escalation. [DOC]

## Canonical Register Fields

| Field | Purpose |
|-------|---------|
| `id` | Stable identifier for cross-reference |
| `title` | Human-readable knowledge item |
| `type` | Decision, runbook, policy, insight, task, glossary, handoff, or risk |
| `source_path` | Local source artifact or documented source id |
| `evidence_tag` | `[CÓDIGO]`, `[DOC]`, `[CONFIG]`, `[INFERENCIA]`, or `[SUPUESTO]` |
| `owner` | Person, team, or escalation route accountable for upkeep |
| `last_reviewed` | ISO date used for decay checks |
| `retrieval_terms` | Search terms that find the item deterministically |
| `status` | `active`, `stale`, `duplicate`, `contradiction`, `gap`, or `deprecated` |
| `next_action` | Concrete maintenance action |

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Evidence coverage | 100% | Every register item has an allowed evidence tag |
| Source coverage | 100% | Every non-gap item has `source_path` |
| Searchability | >= 2 terms/item | Retrieval terms are present and unique enough |
| Decay determinism | 100% | All freshness decisions use `reference_date` |
| Actionability | 100% | Each gap/stale/contradiction has owner and next action |

## Anti-Patterns

- "Knowledge exists in the chat" without durable source. [DOC]
- "Review soon" without owner or date. [DOC]
- Decay status based on "today", "recently", or another moving reference. [DOC]
- Search terms that only repeat the skill name. [DOC]

## References
- `assets/knowledge-taxonomy.json`
- `assets/searchability-policy.json`
- `assets/freshness-policy.json`
- `assets/report-contract.json`
