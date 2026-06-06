# Context Optimizer

Manage token budget during active work by deciding what to load, compress,
defer, or preserve. The skill produces a deterministic optimization packet for
lazy loading, progressive disclosure, safe compression, and eviction decisions.

## Triggers

- "optimize context"
- "reduce token usage"
- "manage context window"
- "lazy load references"
- "compress completed work"
- `/jm:optimize-ctx`

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Deterministic Contract

- Keep the active task and active skill at full fidelity.
- Load skill `SKILL.md` before references; load references only when the skill is active.
- Compress completed or low-relevance artifacts with retention summaries.
- Do not evict risk-flagged, unresolved, or high-relevance material.
- Compute token reduction and utilization from supplied counts.
- Validate JSON optimization packets with `bash skills/context-optimizer/scripts/check.sh`.

## Output Format

Markdown or JSON with context snapshot, loading plan, compression plan, eviction plan, metrics, validation, and risks.
