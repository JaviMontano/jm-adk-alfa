# Input Analyst — Knowledge Graph

## Core Concepts
- input-analyst: primary capability
- validation-gate: quality control checkpoint
- evidence-tagging: [CODE]/[INFERENCE]/[OPEN]/[DOC] claims
- offline-compiler: deterministic local analysis contract
- actionability-score: execution readiness signal
- ambiguity-register: blocking questions and impact

## Dependencies
- Upstream: raw user input, local context, routing policy
- Downstream: task-engine, excellence-loop, selected specialist skill

## Skill Relationships
`scripts/compile-input-analysis.py` depends on local `assets/` and emits a
stable Markdown or JSON report for downstream routing.
