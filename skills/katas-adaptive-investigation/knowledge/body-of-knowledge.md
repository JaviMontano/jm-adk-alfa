<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Adaptive Investigation Body of Knowledge

## Canon

Kata 19 · Investigacion Adaptativa (Descomposicion Dinamica). En dominio desconocido no se planifica al detalle de antemano; se descubre la forma del problema antes de comprometer esfuerzo.

Conceptos clave:

- **Mapeo barato (Fase 1).** `glob` de nombres de archivo + `regex` sobre imports y simbolos. Da la topologia sin leer cuerpos completos.
- **Priorizacion declarada (Fase 2).** Plan ordenado derivado de la topologia, con el porque del orden explicito.
- **Deep-dive selectivo (Fase 3).** Lectura profunda SOLO de los objetivos priorizados.
- **Criterio de re-planificacion.** Re-plan SOLO si un hallazgo INVALIDA el plan; NO si solo lo refina. Esta distincion evita loops de re-planificacion reflejos.
- **Presupuesto de exploracion.** Limite duro de archivos / queries / minutos; al agotarse se reporta encontrado + pendiente.
- **Persistencia.** Plan y findings viven en un scratchpad (Kata 18) para sobrevivir a la ventana de contexto.
- **Paralelismo.** Deep-dives independientes se reparten a subagentes (Kata 4).
- **Contrato offline.** `assets/` define reporte, presupuesto, evidencia, re-plan y scratchpad; `scripts/check.sh` prueba fixtures validos e invalidos sin red.

## Quality Signals

| Signal | Target |
|---|---|
| Presupuesto explicito | Maximo de archivos/queries/minutos definido antes de explorar |
| Criterio de re-plan | Enunciado que distingue invalidar (re-plan) de refinar (no re-plan) |
| Mapeo antes de leer | Topologia barata precede a cualquier deep-dive |
| Deep-dive selectivo | Solo se leen objetivos priorizados, no todo el repo |
| Persistencia | Plan y findings en scratchpad con evidencia |

## Anti-patron canonico

```python
plan = make_full_plan_upfront(repo)
for task in plan:
    do(task)  # nunca se actualiza con la evidencia
```

Variantes del mismo error: `read_all_files()` sin budget; `re_plan()` en cada turno por reflejo en vez de por invalidacion.

## Deterministic Validation

- Aceptar solo reportes que declaran `budget.files`, `budget.queries` y `budget.minutes` con `used <= limit`.
- Exigir `Glob` y `Grep` en `topology.cheap_mapping` antes de cualquier finding de deep-dive.
- Exigir que cada `prioritized_plan.target` provenga de `topology.candidates`.
- Permitir `replans[]` solo cuando el `trigger_finding_id` apunta a un finding con `invalidates_hypothesis=true`.
- Rechazar reportes que requieren red, random, evidencia de reloj o lectura total del repositorio.

## Quiz canonico

Patron de respuestas: **C · B · B**.

- P1: el orden correcto es mapeo barato -> priorizacion -> deep-dive selectivo -> re-plan cuando un hallazgo invalida.
- P3: al agotar presupuesto sin cerrar, reportar lo encontrado y lo pendiente, y escalar a humano usando el scratchpad como evidencia.
