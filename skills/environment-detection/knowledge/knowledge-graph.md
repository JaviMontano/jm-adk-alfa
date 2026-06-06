# Environment Detection Knowledge Graph

## Core Concepts
- environment-detection: startup skill that classifies host, model tier, and safe orchestration.
- local-signal: file, tool, or runtime fact collected without network/time/random dependency.
- capability-profile: supported read/write/shell/subagent/hook/MCP/network set.
- triad-mode: full, sequential, checklist, suggestion, or conservative fallback.
- model-tier: heavy, medium, light, or unknown based on context budget.
- loading-plan: L1/L2/L3/SKIP bootstrap resource plan.
- validation-report: JSON artifact checked offline.

## Edges
- local-signal -> capability-profile -> triad-mode
- model-context -> model-tier -> loading-plan
- conflict -> warn-status -> conservative-fallback
- validation-report -> offline-validator -> Guardian decision

## Guardrails
- Full triad requires actual subagent and hook/MCP evidence.
- Unknown model tier blocks full-history and all-skills L3 loading.
- Conflicts reduce confidence and force `warn`.
