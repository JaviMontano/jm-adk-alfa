---
name: firma-pdf-legal
version: 0.1.0
description: "Coloca una firma manuscrita sobre la linea correcta de un PDF legal con mencion y verificacion por render."
owner: "JM Labs"
triggers:
  - firma-pdf-legal
  - firmar-pdf
  - sign-pdf
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Firma Pdf Legal

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

`scripts/sign_pdf.py --pdf <in> --signature <png> --out <out> --anchor "Firma" --mention "Leída y aprobada"` places the signature above the anchored line and renders a verification PNG. Exit 2 if anchor absent. Deterministic checks: `scripts/check.sh` + fixtures.

## Related Skills

- `validar-liquidacion-co`
- `proceso-seleccion-orchestrator`

## Evidence Requirements

- Cite code, config, docs, or tests used to justify findings.
- Mark inferences and assumptions explicitly.

## Update-Safety Notes

- Generated support files are missing-only by default.
- Use `--force` only after reviewing diffs.
