---
name: session-lifecycle-management
version: 1.0.0
description: "Decidir resume vs fork vs fresh con summary tipado segun validez de contexto y deteccion de tool results stale."
owner: "JM Labs"
triggers:
  - session lifecycle management
  - resume vs fork
  - fresh summary session
  - stale context
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Session Lifecycle Management

## Capacidad

Diseñar e implementar el manejo del ciclo de vida de una sesión de agente, decidiendo de forma explícita entre tres transiciones: `resume` cuando el contexto sigue siendo válido, `fork` cuando se quieren explorar ramas paralelas sin interferencia, y `fresh` con un summary tipado cuando el mundo cambió y los tool results del scratchpad quedaron stale. La capacidad produce un mecanismo de decisión auditable, no una intuición ad hoc del modelo.

El núcleo de ingeniería es la **detección de staleness**: identificar cuándo los resultados cacheados (lecturas de archivo, salidas de comandos, estados de build) ya no reflejan el estado actual del mundo, y emitir un `TypedSummary` que comprima el scratchpad en hechos verificables en lugar de pegar un transcript crudo.

## Cuándo usarla

- Estás construyendo un agente de larga duración que debe sobrevivir a múltiples turnos o reinicios y necesita decidir si reusar el contexto previo.
- Hubo un refactor, migración o despliegue masivo entre dos turnos y dudas si el contexto en memoria sigue siendo confiable.
- Quieres explorar varias hipótesis de solución en paralelo sin que un experimento contamine el contexto del otro.
- El scratchpad creció tanto que pegarlo completo es caro y ruidoso; necesitas un summary tipado.

## Cómo construir

1. **Define el contrato de validez de contexto.** Modela qué hace que un `SessionContext` sea válido: timestamp de captura, conjunto de tool results con su hash o `mtime` de origen, y los invariantes del mundo (HEAD de git, hash del lockfile, esquema de BD).
2. **Implementa el detector de staleness.** Compara cada tool result cacheado contra su fuente actual. Si el `mtime`/hash divergió, marca ese result como `stale`. Una sola dependencia stale crítica invalida el `resume`.
3. **Codifica la matriz de decisión resume/fork/fresh.** Reglas explícitas: contexto válido y objetivo continuo → `resume`; objetivo ramificable sin interferencia → `fork`; staleness crítico o mundo cambiado → `fresh`.
4. **Diseña el `TypedSummary`.** En vez de transcript crudo, emite un objeto tipado: `goal`, `decisions[]`, `open_questions[]`, `verified_facts[]`, `stale_dropped[]`. Cada hecho conserva su evidencia y se descartan los results stale.
5. **Aísla los forks.** Garantiza que cada rama tenga su propio scratchpad y workspace para que dos forks no compartan estado mutable.
6. **Valida con el checklist y registra la decisión.** La transición elegida debe quedar trazada con su razón (qué disparó el `fresh`, qué quedó stale).

## Patrón correcto

```python
# GOOD: decision explicita basada en validez de contexto + staleness tipado
def decide_transition(ctx: SessionContext, goal: Goal) -> Transition:
    stale = [tr for tr in ctx.tool_results if is_stale(tr)]  # mtime/hash vs origen
    if any(tr.critical for tr in stale):
        # el mundo cambio: no reusar, sintetizar y reiniciar
        return Fresh(summary=typed_summary(ctx, drop=stale))
    if goal.is_branchable and not goal.shares_mutable_state:
        return Fork(branches=goal.hypotheses, isolated_scratchpad=True)
    return Resume(ctx)  # contexto valido y objetivo continuo


def typed_summary(ctx: SessionContext, drop: list[ToolResult]) -> TypedSummary:
    dropped_sources = {d.source for d in drop}
    return TypedSummary(
        goal=ctx.goal,
        decisions=ctx.decisions,
        open_questions=ctx.open_questions,
        verified_facts=[f for f in ctx.facts if f.source not in dropped_sources],
        stale_dropped=list(dropped_sources),
    )
```

## Anti-patrón

```python
# ANTI: resume ciego tras un refactor masivo + transcript crudo como "summary"
def next_session(prev_transcript: str, goal: Goal) -> Session:
    # 1) Reusa el contexto sin verificar si los archivos cambiaron (resume tras refactor).
    # 2) Pega el transcript completo viejo: ruido, tokens, y tool results stale
    #    que el modelo tratara como verdad actual.
    return Session(context=prev_transcript, goal=goal)
```

## Checklist de validación

- [ ] ¿Se detectaron los tool results stale comparando contra la fuente actual (mtime/hash/HEAD)?
- [ ] ¿El summary es tipado (goal, decisions, open_questions, verified_facts, stale_dropped) y no un transcript crudo?
- [ ] ¿Los forks corren sin interferencia, con scratchpad y workspace aislados?
- [ ] ¿La transición resume/fork/fresh quedó trazada con su razón?
- [ ] ¿Una dependencia stale crítica fuerza `fresh` en lugar de `resume`?

## Katas y skills relacionadas

- Kata 25 — decisión de ciclo de vida de sesión.
- `katas-session-resume-fork`
- `workspace-governance`
- `workflow-forge`
- `quality-guardian`
