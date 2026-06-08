---
name: red-y-referencias
version: 0.1.0
description: "Gestiona referencias con consentimiento explicito, follow-ups y mapa de red."
owner: "JM Labs"
triggers:
  - red-y-referencias
  - referencias
  - networking
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Red Y Referencias

## Inputs Expected

- Goal or task to complete.
- Relevant context, constraints, and audience.
- Existing files or references when the request depends on a codebase or document.

## Outputs Expected

- A concise deliverable in the requested format.
- Evidence notes for non-obvious claims.
- Validation status and remaining risks.

## Procedure

### Discover

Read the user request, inspect relevant project artifacts, and identify missing critical information.

### Analyze

Map intent to the skill domain, choose the smallest viable approach, and identify risks before execution.

### Execute

Produce the deliverable using the allowed tools and keep changes scoped to the request.

### Validate

Check quality criteria, edge cases, assumptions, and evidence requirements before final delivery.

## Quality Criteria

- The output directly addresses the user goal.
- Claims are tagged with evidence when required by the host environment.
- No local overrides or generated files are overwritten without explicit force.
- The result is actionable and has clear acceptance criteria.

## Edge Cases

- Empty input: ask for the missing objective.
- Conflicting requirements: state the conflict and choose the safer interpretation.
- Local customization: preserve local files and prefer additive changes.

## Assumptions and Limits

- This skill does not replace expert review for high-risk legal, medical, financial, or security decisions.
- If evidence is unavailable, mark the claim as an assumption or open question.

## Scripts

`scripts/consent_check.py --input <json>` blocks references without explicit consent and flags stale follow-ups (>30d). Exit 1 if a non-consented ref is present. Deterministic checks: `scripts/check.sh` + fixtures.

## Related Skills

- `onboarding-90-dias`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Cite code, config, docs, or tests used to justify findings.
- Mark inferences and assumptions explicitly.

## Update-Safety Notes

- Generated support files are missing-only by default.
- Use `--force` only after reviewing diffs.
