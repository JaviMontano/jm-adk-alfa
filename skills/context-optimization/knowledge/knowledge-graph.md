# Context Optimization Knowledge Graph

## Core Concepts
- context-budget: maximum usable tokens for the active turn or handoff.
- progressive-loading: L1 metadata, L2 operational summary, L3 full resource load.
- relevance-score: deterministic 0.0 to 1.0 rating used to justify load depth.
- pruning-risk: low, medium, or high risk of losing evidence or future task continuity.
- session-state: summarized handoff facts that survive context compaction.
- validation-report: JSON artifact checked offline against the optimization contract.

## Dependencies
- Upstream: active task, current context inventory, evidence obligations, session-state policy.
- Downstream: optimized prompt pack, handoff summary, validation evidence, residual-risk note.

## Guardrails
- Only one active skill receives L3 by default.
- L3 requires relevance >= 0.70.
- Pruning is allowed only when risk is `low`.
- Full transcript persistence is never authorized by this skill.
