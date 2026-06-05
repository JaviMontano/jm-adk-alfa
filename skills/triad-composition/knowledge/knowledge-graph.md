# Triad Composition — Knowledge Graph

## Core Concepts

- `triad-composition`: deterministic role selection for non-trivial Pristino tasks.
- `composition-matrix`: domain-to-Lead/Support/Guardian mapping.
- `classification-policy`: confidence bands and tie-breakers.
- `degraded-mode-policy`: explicit partial-delivery behavior.
- `triad-output-contract`: required packet sections and blocked phrases.

## Flow

Input request -> required inputs -> domain scoring -> confidence band -> selected triad or clarification -> G0-G3 validation.

## Skill Relationships

- Upstream: `auto-prompt-matching`, `input-tolerance`.
- Peer: `intelligent-routing`, `constitution-compliance`, `socratic-debate`.
- Downstream: domain Lead skill, Support review skill, Guardian validation skill.
