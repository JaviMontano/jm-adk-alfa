---
name: context-optimization-deep
type: variation
version: 2.0.0
description: "Context Optimization — deep analysis mode."
---
# Context Optimization — Deep Mode

## Execution
1. Build a complete resource inventory with relevance, evidence criticality, freshness, and dependency notes.
2. Compare naive full-loading against the proposed L1/L2/L3/prune plan.
3. Analyze false-positive risk: resources that look relevant by name but lack task-specific evidence.
4. Analyze degradation risk: required evidence, handoff state, or validation context that could be lost.
5. Produce machine-readable JSON for offline validation when the user needs a repeatable artifact.
6. Require confidence >= 0.95 only when backed by explicit metrics and validation evidence.
