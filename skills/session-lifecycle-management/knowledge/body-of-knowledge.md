<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Session Lifecycle Management Body of Knowledge

## Canon

El ciclo de vida de una sesión de agente se gobierna con tres transiciones tipadas:

- **resume:** el `SessionContext` previo sigue siendo válido (objetivo continuo, ningún tool result crítico stale). Se reusa tal cual.
- **fork:** el objetivo es ramificable y las ramas no comparten estado mutable. Cada fork corre con scratchpad y workspace aislados para que un experimento no contamine al otro.
- **fresh:** el mundo cambió (refactor, migración, despliegue) o el scratchpad creció demasiado. No se reusa el contexto crudo; se emite un `TypedSummary` y se reinicia.

**Conceptos clave:**

- **SessionContext:** snapshot con timestamp, tool results y sus fuentes, e invariantes del mundo (HEAD de git, hash de lockfile, esquema de BD).
- **Staleness detection:** comparar cada tool result cacheado contra su fuente actual vía mtime/hash/HEAD. Una dependencia stale crítica invalida el `resume`.
- **TypedSummary:** objeto serializable con `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]`, `stale_dropped[]`. Reemplaza al transcript crudo.
- **Fork isolation:** garantía de que dos ramas no escriben sobre el mismo estado mutable.

## Quality Signals

| Signal | Target |
|---|---|
| Staleness coverage | Todo tool result cacheado tiene señal de frescura contra su fuente |
| Summary tipado | El handoff es un objeto tipado, nunca un transcript crudo |
| Fork isolation | Ningún par de forks comparte estado mutable |
| Trazabilidad | La transición elegida queda registrada con su razón |

## Decisión de diseño

Cuando hay duda entre `resume` y `fresh`, el default seguro es `fresh` con `TypedSummary`: reusar contexto stale corrompe al agente con hechos falsos, mientras que sintetizar de más solo cuesta algo de recall recuperable. El costo de un falso `resume` es mayor que el de un falso `fresh`.

## Anti-patrón

`resume` ciego tras un refactor masivo, y pegar el transcript completo viejo como si fuera el contexto: introduce tokens de ruido y tool results stale que el modelo tratará como verdad actual.

## Open Knowledge

- Heurísticas de costo: a partir de qué tamaño de scratchpad conviene `fresh` aunque el contexto siga válido.
- Catálogo de señales de staleness por tipo de fuente (archivo, git, paquete, BD, API externa).
