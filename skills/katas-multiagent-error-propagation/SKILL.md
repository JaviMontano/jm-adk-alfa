---
name: katas-multiagent-error-propagation
version: 1.0.0
description: "Propagacion de errores multi-agente: distinguir access failure de valid empty, local recovery primero y coverage gap annotation."
owner: "JM Labs"
triggers:
  - multiagent error propagation
  - access failure vs empty
  - coverage gap
  - local recovery
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Multiagent Error Propagation

## Qué es

En una arquitectura hub-and-spoke, un coordinador delega búsquedas en subagentes. Cuando un subagente falla, debe propagar el error al coordinador con **contexto estructurado**, no un payload silencioso. El contrato mínimo de propagación es:

`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`.

Cuatro reglas gobiernan la propagación:

1. **Local recovery primero** — el subagente reintenta fallos transitorios (broaden query, longer timeout) antes de propagar.
2. **Distinguir access failure de valid empty** — un timeout o un permission denied NO es lo mismo que una búsqueda que devolvió 0 matches legítimamente.
3. **Coverage gap annotation** — cuando un dominio queda sin cubrir, se anota explícitamente en el synthesis del coordinador.
4. **Nunca enmascarar error como success vacío** — un fallo nunca se devuelve como `{results:[]}`.

## Por qué importa (falla que evita)

Devolver `{results:[]}` en un timeout hace que el coordinador asuma "no había información" y produzca un report confiado con un **hueco silencioso**: el usuario recibe una respuesta que parece completa pero omite una fuente que simplemente falló. Por el otro extremo, un genérico `'search unavailable'` priva al coordinador del contexto (`attempted_query`, `suggested_alternatives`) necesario para decidir alternativas o anotar el gap. Ambos modos rompen la confiabilidad del synthesis multi-agente.

## Modelo mental

- **Local recovery primero:** el subagente reintenta transients (broaden, longer timeout) antes de escalar al coordinador.
- **Access failure != valid empty:** timeout/permission = el sistema no pudo mirar; search OK con 0 matches = el sistema miró y no había nada. Señales y manejo distintos.
- **Coverage gap annotation:** si una fuente no se pudo consultar, el synthesis lo declara explícitamente; no se infiere ausencia de datos.
- **Nunca enmascarar:** un error de acceso jamás se serializa como un success vacío. `success:False` con contexto, o `success:True, empty_valid:True`.
- **`retryable=False` (permission)** es una señal explícita: escalar / anotar coverage gap, no reintentar la misma query.

## Patrón correcto

```python
# Subagente: propagación estructurada con local recovery
def search_subagent(query):
    try:
        results = http_search(query, timeout=10)
        if not results:
            return {"success": True, "results": [], "empty_valid": True}
        return {"success": True, "results": results}
    except TimeoutError:
        try:
            return {"success": True, "results": broaden(query)}  # local recovery
        except Exception:
            return {
                "success": False,
                "failure_type": "timeout",
                "attempted_query": query,
                "partial_results": [],
                "suggested_alternatives": ["broaden terms", "longer timeout"],
            }
    except PermissionError as e:
        return {
            "success": False,
            "failure_type": "permission",
            "retryable": False,
            "explanation": str(e),
        }
```

## Anti-patrón

```python
# Enmascara el error como success vacío:
# el coordinador asume "no había info" y escribe un report con hueco silencioso.
def search_subagent(query):
    try:
        return {"results": http_search(query, timeout=10)}
    except Exception:
        return {"results": []}
```

## Argumento de certificación

- Distinguir **access failure** de **valid empty** y manejarlos por ramas separadas.
- Defender **local recovery** + **propagación estructurada** (failure_type, attempted_query, partial_results, suggested_alternatives).
- Insistir en **coverage gap annotation** explícita en el synthesis.
- Rechazar enmascarar errores como success vacío y rechazar el genérico `'search unavailable'`.
- Reconocer `retryable=False` (permission) como señal de escalar/anotar, no de reintentar la misma query.

## Cuándo activar

- Diseño o revisión de arquitecturas hub-and-spoke / multi-agente donde un coordinador sintetiza resultados de subagentes.
- Cuando un report multi-agente "se ve completo" pero podría tener huecos silenciosos por fallos de fuente.
- Diferenciar manejo de timeout/permission vs búsqueda vacía válida.
- Escenarios de Customer Support y Multi-Agent con orquestación de búsquedas.

## Skills relacionadas

- `katas-mcp-structured-errors`
- `katas-validation-retry-feedback`
- `katas-critical-self-correction`
- `katas-independent-reviewer-multipass`
