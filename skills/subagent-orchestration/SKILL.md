---
name: subagent-orchestration
version: 1.0.0
description: "Orquestar coordinadores hub-and-spoke con AgentDefinition y Task, contexto aislado por subagente y propagacion de errores estructurada."
owner: "JM Labs"
triggers:
  - subagent orchestration
  - hub and spoke
  - coordinator agents
  - error propagation
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Subagent Orchestration

## Capacidad

Diseñar coordinadores hub-and-spoke que despachan subagentes aislados mediante `AgentDefinition` + `Task` y agregan sus resultados con errores estructurados. Cada subagente corre en una sesión nueva con contexto vacío, su propio conjunto de tools y su propio modelo (por ejemplo Haiku barato para extracción), y el coordinador recibe únicamente el último mensaje de cada uno. La capacidad clave es contener el blast radius: si un spoke falla, devuelve un error tipado que el hub puede interpretar y anotar como gap de cobertura, nunca como un `success` vacío que contamine la agregación.

## Cuándo usarla

- Una tarea se descompone en subtareas independientes que se benefician de aislamiento de contexto (cada una arranca limpia, sin arrastrar el ruido de las demás).
- Hay subtareas baratas y repetitivas (extracción, clasificación) que conviene delegar a un modelo más económico que el coordinador.
- Necesitas distinguir entre "la fuente no existe / no se pudo acceder" y "la fuente existe pero está vacía", porque ambas colapsan a `[]` si no se modela el error.
- El fallo parcial de una rama no debe abortar ni corromper el resultado global.

## Cómo construir

1. Define el contrato del coordinador: qué subtareas existen, qué tool/modelo recibe cada spoke y qué shape de resultado espera el hub al agregar.
2. Declara cada subagente como `AgentDefinition` con su `prompt`, sus `tools` mínimas y su `model` (Haiku para extracción de bajo costo; Sonnet para razonamiento).
3. Despacha con `Task` de forma que cada subagente sea una sesión nueva con contexto vacío; el coordinador solo consume el último mensaje devuelto, no el transcript.
4. Diseña el error estructurado del spoke: `failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`. Intenta local recovery primero (reintento acotado, query alternativa) antes de propagar.
5. En la agregación, trata `access_failure` distinto de `valid_empty`: anota un coverage gap explícito en el resultado del hub y nunca enmascares el error como `success` con lista vacía.
6. Acota el blast radius: un spoke que cae no debe tumbar al resto; el hub continúa y reporta cobertura parcial con la rama afectada identificada.

## Patrón correcto

```python
# GOOD: hub-and-spoke con aislamiento y error tipado por spoke
async def run_spoke(query: str) -> dict:
    try:
        results = await search(query)  # subagente aislado, tools mínimas
        if results is None:            # acceso falló, no es "vacío válido"
            return {
                "failure_type": "access_failure",
                "attempted_query": query,
                "partial_results": [],
                "suggested_alternatives": [broaden(query)],
            }
        return {"status": "ok", "results": results}  # [] aquí = empty válido
    except RateLimitError as e:
        return {
            "failure_type": "rate_limited",
            "attempted_query": query,
            "partial_results": [],
            "suggested_alternatives": ["retry_after:" + str(e.retry_after)],
        }

async def coordinator(queries: list[str]) -> dict:
    spokes = await asyncio.gather(*(run_spoke(q) for q in queries))
    aggregated, gaps = [], []
    for q, s in zip(queries, spokes):
        if s.get("failure_type"):
            gaps.append({"query": q, "reason": s["failure_type"]})  # blast radius acotado
        else:
            aggregated.extend(s["results"])
    return {"results": aggregated, "coverage_gaps": gaps}  # gap explícito, no oculto
```

## Anti-patrón

```python
# ANTI: un solo agente con todo concatenado + error enmascarado como vacío
def mega_agent(all_queries):
    context = "\n".join(read_everything())   # sin aislamiento, contexto saturado
    out = []
    for q in all_queries:
        try:
            out += search(q)
        except:                              # error swallow
            return {"results": []}           # access-failure indistinguible de empty
    return {"results": out}                  # sin coverage gap, sin blast radius
```

## Checklist de validación

- ¿Aislamiento estructural? Cada spoke arranca con contexto vacío y tools/modelo propios; el hub solo ve el último mensaje.
- ¿Blast radius acotado? El fallo de un spoke no aborta ni corrompe la agregación del resto.
- ¿Los errores distinguen `access_failure` de `valid_empty`? `[]` por acceso fallido nunca se confunde con `[]` legítimo.
- ¿Coverage gap explícito? El resultado del hub anota qué ramas quedaron sin cobertura y por qué.
- ¿Se intentó local recovery antes de propagar (reintento/alternativa acotados)?
- ¿Ningún `except` enmascara un error como `success` vacío?

## Katas y skills relacionadas

- Katas: `04`, `28`.
- Relacionadas: `katas-hub-and-spoke-isolation`, `katas-multiagent-error-propagation`, `structured-output-design`, `prompt-chaining-design`, `human-escalation-design`.
