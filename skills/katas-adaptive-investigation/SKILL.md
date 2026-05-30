---
name: katas-adaptive-investigation
version: 1.0.0
description: "Investigacion adaptativa: mapeo barato, budget de exploracion acotado y re-plan disciplinado solo al invalidar la hipotesis."
owner: "JM Labs"
triggers:
  - adaptive investigation
  - dynamic decomposition
  - exploration budget
  - re-plan discipline
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 19 · Investigacion Adaptativa (Descomposicion Dinamica)

## Que es

En un dominio desconocido no se planifica al detalle de antemano. El agente mapea la topologia primero (un `glob` barato sobre nombres de archivo, `regex` sobre imports y simbolos), genera un plan priorizado a partir de esa topologia, y re-adapta el plan cuando un hallazgo invalida la hipotesis vigente. Todo el ciclo ocurre dentro de un presupuesto de exploracion acotado: un maximo duro de archivos, queries o minutos.

Escenarios donde aplica: Multi-Agent Orchestration, Dev Productivity, Code Generation.

## Por que importa (falla que evita)

Un plan rigido en territorio desconocido garantiza desperdicio: el agente sigue ramas muertas porque "estaba en el plan", no porque la evidencia las sostenga. La investigacion adaptativa prioriza la atencion sobre lo que la realidad muestra, no sobre lo que la hipotesis inicial asumio. Sin presupuesto, ademas, el agente quema contexto leyendo el repo entero antes de tener una sola pregunta enfocada.

## Modelo mental

- **Fase 1 - mapeo barato.** Escanear la topologia con `glob` de nombres y `regex` de imports/simbolos. Sin leer cuerpos completos todavia.
- **Fase 2 - priorizacion declarada.** Construir un plan ordenado a partir de la topologia y enunciar por que cada objetivo esta arriba.
- **Fase 3 - deep-dive selectivo.** Leer en profundidad SOLO los objetivos priorizados, nunca todo.
- **Re-planificar SOLO si un hallazgo INVALIDA el plan**, no si solo lo refina. Esto evita loops de re-planificacion reflejos en cada turno.
- **Presupuesto duro.** Maximo de archivos, queries y minutos; cuando se agota, se reporta lo encontrado y lo pendiente.
- **Persistir plan y findings en un scratchpad** (ver `katas-scratchpad-pattern`, Kata 18) para que el estado sobreviva al contexto.

## Patron correcto

```python
topology = scan_repo(globs=['src/**/*.py'])
budget = Budget(files=50, queries=20)
plan = prioritize(topology)
while plan and budget.remaining():
    target = plan.pop()
    finding = deep_dive(target, budget)
    scratchpad.append('Hallazgos', finding)
    if finding.invalidates(plan):
        plan = re_plan(topology, finding)
```

## Anti-patron

```python
# Plan rigido upfront: nunca se actualiza con la evidencia
plan = make_full_plan_upfront(repo)
for task in plan:
    do(task)

# o leer todo sin presupuesto
read_all_files()

# o re_plan() en cada turno por reflejo, no por invalidacion
```

## Argumento de certificacion

- Definir un presupuesto de exploracion explicito (archivos / queries / minutos).
- Enunciar el criterio de re-planificacion: que dispara un re-plan (un hallazgo que invalida la hipotesis) y que NO lo dispara (un hallazgo que solo la refina).
- Conectar con Kata 4 (subagentes para deep-dive paralelo) y Kata 18 (scratchpad como memoria persistente del plan y los findings).

## Cuando activar

- El dominio o repositorio es desconocido y no hay mapa previo confiable.
- El usuario pide investigar, mapear, auditar o entender una base de codigo o documento extenso.
- Hay riesgo de quemar contexto leyendo de mas si no se acota la exploracion.
- No activar cuando la tarea ya esta totalmente especificada y el plan es trivial y estable.

## Skills relacionadas

- `katas-subagent-parallelism`
- `katas-scratchpad-pattern`
- `katas-builtin-tool-selection`
- `katas-plan-mode-exploration`
