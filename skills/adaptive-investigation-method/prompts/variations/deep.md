# Adaptive Investigation Method Deep Variation

Usar cuando el dominio es amplio, el objetivo ambiguo o las consecuencias cruzan muchos archivos.

1. Fija un `budget` mayor y registra cada decremento explicitamente.
2. Construye un mapa de superficie multinivel (estructura + senales por `Grep`).
3. Mantiene la lista de hipotesis viva: re-prioriza cada vez que un finding invalide la hipotesis activa, y deja traza de cada re-plan.
4. Documenta los nodos descartados y por que, para que la decision sea auditable.
5. Si el mundo cambia a mitad de camino (refactor, datos stale), considera `session-lifecycle-management` (fork/fresh).

Incluye: notas de descubrimiento, hipotesis consideradas y descartadas, deep-dives con evidencia, decisiones de re-plan, deliverable y riesgos.
