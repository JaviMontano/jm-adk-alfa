# Auto Prompt Matching - Knowledge Graph

## Core Concepts

- auto-prompt-matching: deterministic routing capability
- routing-source: inspected index, prompt metadata, or skill file
- candidate-score: trigger, purpose, scope, penalty, and tie-break evidence
- confidence-band: route, ask, or decline
- coverage-gap: missing or stale source that limits route certainty
- downstream-separation: routing decision does not execute the selected skill

## Dependencies

- Upstream: input-analyst, context-optimization
- Downstream: workflow-orchestration, output-contract-enforcer

## Skill Relationships

Part of the JM Labs canonical skill registry and orchestration layer.
