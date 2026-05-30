<!--
generated-by: scripts/scaffold-skill.py
generated-for: subagent-orchestration
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Coordinador hub-and-spoke: un spoke `finder` (búsqueda) y un spoke `extractor` (extracción con modelo barato) por empresa; el hub agrega distinguiendo acceso fallido de vacío legítimo y reporta coverage gaps.

## Spoke design

| Spoke | Subtarea | Tools | Modelo |
|---|---|---|---|
| finder | localizar sitio | WebFetch | haiku |
| extractor | sector + headcount | Read | haiku |
| ranker | priorización final | (agregado) | sonnet |

## Coordinator (GOOD pattern)

```python
async def enrich_company(name: str) -> dict:
    site = await finder_spoke(name)          # sesion aislada, contexto vacio
    if site is None:                         # acceso fallido, NO vacio valido
        return {
            "failure_type": "site_not_found",
            "attempted_query": name,
            "partial_results": [],
            "suggested_alternatives": [name + " careers"],
        }
    try:
        fields = await extractor_spoke(site)  # haiku barato
    except RateLimitError as e:
        return {
            "failure_type": "rate_limited",
            "attempted_query": name,
            "partial_results": [],
            "suggested_alternatives": ["retry_after:" + str(e.retry_after)],
        }
    return {"status": "ok", "sector": fields.sector, "headcount": fields.headcount}

async def coordinator(names: list[str]) -> dict:
    spokes = await asyncio.gather(*(enrich_company(n) for n in names))
    rows, gaps = [], []
    for n, s in zip(names, spokes):
        if s.get("failure_type"):
            gaps.append({"company": n, "reason": s["failure_type"]})  # blast radius acotado
        else:
            rows.append(s)
    return {"rows": rows, "coverage_gaps": gaps}  # gap explicito
```

## Anti-pattern (rejected)

```python
# ANTI: un solo agente, todo el HTML concatenado, error enmascarado
def enrich_all(names):
    blob = "\n".join(fetch_everything(names))  # contexto saturado, sin paralelizar
    out = []
    for n in names:
        try:
            out.append(extract(blob, n))
        except:
            return {"rows": []}                # site_not_found indistinguible de vacio
    return {"rows": out}                       # sin coverage gaps
```

## Validation

- Aislamiento estructural: cada spoke es sesión nueva con tools mínimas. OK
- Blast radius acotado: el fallo de una empresa solo agrega un coverage gap. OK
- access_failure != valid_empty: `site_not_found` y `rate_limited` son tipos distintos de un headcount ausente legítimo. OK
- Coverage gap explícito: `coverage_gaps` lista empresa + razón. OK
- Sin error swallowed: ningún `except` devuelve éxito vacío. OK

## Risks and limits

- Rate limits del finder pueden inflar coverage gaps; conviene reintento con backoff antes de propagar.
- Si la fuente HTML cambia de formato, el extractor puede degradar silenciosamente; añadir self-correction sobre campos numéricos.
