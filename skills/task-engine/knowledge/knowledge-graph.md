# Task Engine — Knowledge Graph

## Core Concepts

- `task-engine`: deterministic DSVSR reasoning.
- `activation-policy`: decides fast path, full DSVSR, or clarification.
- `confidence-scale`: maps scores to evidence requirements.
- `reflection-policy`: governs below-target retries and stop conditions.
- `dsvsr-packet-contract`: validates output shape and blocked phrases.

## Flow

Problem -> activation decision -> decomposition -> sub-problem solve -> verification -> synthesis -> reflection -> reasoning metadata.

## Skill Relationships

- Upstream: `input-analyst`, `context-optimization`.
- Peer: `confidence-calibration`, `assumption-log`, `quality-gatekeeper`.
- Downstream: domain-specific implementation or report skill.
