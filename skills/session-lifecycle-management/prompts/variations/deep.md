<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Deep Variation

Úsala cuando hubo cambios grandes (refactor, migración, despliegue), el scratchpad es enorme, o hay múltiples forks con riesgo de interferencia.

## Discovery

- Inventaria cada tool result cacheado y su fuente; clasifica cada fuente como crítica o no.
- Captura los invariantes del mundo: HEAD de git, hash del lockfile, esquema de BD, versión de API externa.

## Staleness analysis

- Para cada fuente, define la señal de frescura adecuada y compárala contra el snapshot.
- Busca staleness transitiva: un archivo no tocado que depende de otro que sí cambió.

## Options considered

- `resume`: justifica por qué ningún result crítico está stale.
- `fork`: demuestra el aislamiento (scratchpad y workspace por rama).
- `fresh`: enumera qué disparó el reinicio y qué entró en `stale_dropped`.

## Output

Incluye notas de discovery, la evidencia de staleness por fuente, la transición elegida, el `TypedSummary` completo si aplica, la validación contra el checklist y los riesgos residuales.
