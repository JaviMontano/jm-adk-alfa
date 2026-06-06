# Context Window Management — Body of Knowledge

## Canon

Context Window Management is a deterministic budgeting discipline. It treats
context as an inventory of items with source IDs, token estimates, priority
tiers, and retention actions. The goal is to fit the available context budget
without losing active instructions, decisions, blockers, validation evidence, or
open questions.

## Priority Tiers

| Tier | Preserve Because | Default Action |
|---|---|---|
| P0 | Current user intent, branch/PR state, blockers, validation evidence. | keep |
| P1 | Active implementation files and current skill contracts. | keep or structured summary |
| P2 | Supporting docs and adjacent references. | compress |
| P3 | Historical, redundant, or archival context. | reference or evict |

## Compression Methods

| Method | Use When | Requirement |
|---|---|---|
| `extractive-summary` | Exact phrases or IDs matter. | Preserve cited facts verbatim enough to verify. |
| `structured-summary` | Multiple decisions or sections need compact form. | Preserve IDs, paths, decisions, blockers, evidence, and open questions. |
| `reference-only` | Source can be reloaded later. | Keep path and reason why full content was dropped. |

## Quality Metrics

| Metric | Target | How to Measure |
|---|---:|---|
| Budget fit | 100% | Post-plan tokens fit available context. |
| P0 safety | 100% | P0 items are never evicted. |
| Compression safety | 100% | Compressed items reduce estimates and preserve required fields. |
| Eviction discipline | 100% | Evictions start with P3 and cite rationale. |
| Offline validation | 100% | `bash skills/context-window-management/scripts/check.sh` passes. |

## Anti-Patterns

- Evicting active instructions or validation evidence.
- Claiming fit without response-token reserve.
- Compression that is longer than the source.
- Summaries that omit IDs, paths, decisions, blockers, or open questions.
- Treating browser window management as context-window management.
