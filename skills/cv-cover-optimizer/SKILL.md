---
name: cv-cover-optimizer
version: 0.1.0
description: "Optimiza CV y cover para ATS y voz de marca; extiende cv-transformer con lint de keywords y secciones."
owner: "JM Labs"
triggers:
  - cv-cover-optimizer
  - optimizar-cv
  - ats-cv
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
---

# Cv Cover Optimizer

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

`scripts/ats_lint.py --input <json>` lints CV/cover for ATS keyword coverage, sections, length, contact, and brand voice (stacked trademarks/hustle). Exit 1 on issues. Extends `cv-transformer`. Deterministic checks: `scripts/check.sh` + fixtures.

## Related Skills

- `cv-transformer`
- `gratitud-post-proceso`

## Evidence Requirements

- Cite code, config, docs, or tests used to justify findings.
- Mark inferences and assumptions explicitly.

## Update-Safety Notes

- Generated support files are missing-only by default.
- Use `--force` only after reviewing diffs.
