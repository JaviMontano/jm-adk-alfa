# Body Of Knowledge

## Canon

- Provenance tipada es parte del schema, no una nota opcional.
- `source_registry[]` declara todas las fuentes con `source_id`, `source_name` y `publication_date`.
- Cada `claim` factual debe tener `sources[]` no vacío.
- Cada `source_id` referenciado por un claim debe existir en `source_registry`.
- Los conflictos se preservan con todos los valores contradictorios, `conflict=true`, `needs_human_review=true` y una ruta de escalado.
- La fecha de publicación informa al humano, pero no resuelve automáticamente un conflicto.

## Quality Signals

| Signal | Target |
|---|---|
| No orphan claims | `claims_without_sources=0` |
| Registry integrity | `unknown_source_refs=0` |
| Conflict preservation | `conflicts_silenced=0` |
| Human review | todo conflicto tiene `needs_human_review=true` |
| Auditability | el resultado es verificable claim por claim |

## Anti-Patterns

- Prosa libre sin source IDs.
- Elegir el dato más reciente sin registrar el conflicto.
- Promediar valores contradictorios.
- Crear `resolved_value` en un claim marcado como conflicto.
- Agregar claims de subagentes sin preservar `source_id`.

## Boundaries

- Provenance preserva de dónde viene un dato; no reemplaza verificación numérica.
- Si el problema principal es cálculo, combinar con una skill de verificación numérica.
- Si el problema principal es escalado operativo, usar la ruta humana declarada por el contrato.
