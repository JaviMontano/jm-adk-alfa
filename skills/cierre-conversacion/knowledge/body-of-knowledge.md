# Cierre Conversacion Body Of Knowledge

## Canon

A closeout is not a generic summary. It is a continuity artifact that protects future work from lost decisions, stale state, false completion, and unapproved durable writes.

## Evidence Discipline

Use evidence tags on claims:

- `[CÓDIGO]` for local commands, files, diffs, PR state, or CI output.
- `[CONFIG]` for user instructions and workflow rules.
- `[DOC]` for stable project documentation.
- `[INFERENCIA]` for conclusions derived from observed evidence.
- `[SUPUESTO]` for assumptions that may be wrong.
- `[POR_CONFIRMAR]` for unresolved external or user confirmation.

## Closeout Invariants

- A completed task needs completion evidence.
- A green merge claim needs PR/CI evidence.
- Failed validation remains visible until fixed.
- Durable writes require explicit authority.
- Next handoff must name the next concrete action.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Every claim is tagged or explicitly marked open |
| False completion control | Guardian blocks pass when validation failed |
| Durable update safety | Proposed writes are separate from confirmed writes |
| Handoff clarity | A future session can continue without re-reading raw conversation |
