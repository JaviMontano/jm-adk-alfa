# BMAD Method Output

## BMAD Plan

State project type, routing, and evidence tag.

## Lifecycle Routing

List phase, persona, artifact, and whether the phase is allowed now.

## Persona Routing

Use `assets/persona-matrix.json`.

## Artifact Chain

Use `assets/artifact-chain.json`.

## Readiness Gate

Use `assets/readiness-gate-policy.json`; Phase 4 is allowed only on `PASS`.

## Validation

Run `scripts/validate_bmad_packet.py` for formal packets.

## Risks and Open Questions

Mark missing context as `[OPEN]`; do not fabricate artifacts.
