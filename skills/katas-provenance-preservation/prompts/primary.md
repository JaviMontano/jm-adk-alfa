# Primary Prompt

## Objective

Producir un reporte factual auditable con provenance tipada: no hay claim sin fuente y los conflictos se preservan.

## Required Inputs

- Fuentes con identificador estable, nombre y fecha de publicación.
- Claims o preguntas factuales a responder.
- Valores aportados por cada fuente o subagente.

## Process

1. Construye `source_registry[]`.
2. Emite cada claim con `claim_id`, `claim`, `sources[]` y `conflict`.
3. Rechaza claims huérfanos.
4. Preserva conflictos con todos los valores y `needs_human_review=true`.
5. Valida `claims_without_sources=0`, `unknown_source_refs=0` y `conflicts_silenced=0`.

## Output

Entrega `Summary`, `Source Registry`, `Claims`, `Conflicts`, `Validation` y `Risks And Limits`.
