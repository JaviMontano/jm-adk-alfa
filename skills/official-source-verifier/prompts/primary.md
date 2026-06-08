# Official Source Verifier Primary Prompt

## Objective

Verify a decision against official sources and produce a claim-level evidence packet.

## Required Inputs

- Decision or question that depends on external authority.
- Product, framework, SDK, API or service involved.
- Proposed change and affected scope.
- Any known secondary sources, marked as discovery-only.

## Process

1. Define the exact `question`.
2. Search official sources first: official docs, specs, repositories or vendor-owned references.
3. Register each source with URL, publisher, source type, role and `accessed_date`.
4. Convert findings into claim records. Verified claims require at least one official source id.
5. Mark secondary sources as `role=discovery` or `role=context`; never authority.
6. Authorize a change only when `decision.justified_change` traces to verified claims.
7. Block when official evidence is missing, stale, contradictory without resolution, or unsupported.

## Output

Markdown or JSON with source registry, claims, decision, validation, guardian and risks. When JSON is required, align with `assets/official-source-verifier-contract.json`.
