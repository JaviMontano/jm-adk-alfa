---
name: katas-posttooluse-normalization
version: 1.0.0
description: "Normalizacion de outputs heterogeneos via hook PostToolUse y updatedMCPToolOutput antes de entrar al historial del modelo."
owner: "JM Labs"
triggers:
  - posttooluse normalization
  - output normalization
  - updatedmcptooloutput
  - legacy payload
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Posttooluse Normalization

## Qué es

Kata 03 del kit JM-ADK. Un hook `PostToolUse` intercepta el `tool_response` heterogéneo de tools legacy (XML envuelto, códigos de estado arcanos como `0xA1`) y lo reescribe a JSON canónico mediante `updatedMCPToolOutput` antes de que el output entre al historial del modelo. El modelo nunca ve el XML crudo: ve solo el JSON limpio que el runtime garantiza.

Escenarios canónicos: Customer Support y Legacy ERP Integration.

## Por qué importa (falla que evita)

- Sin normalización central, cada token de XML legacy quema budget de contexto y dispersa la atención del modelo sobre ruido sintáctico.
- Normalizar por-tool (cada tool decide si limpia su salida) es frágil: cualquier wrapper o handler nuevo que olvide aplicar la regla rompe la garantía y envenena el contexto con payloads sucios.
- La normalización de outputs heterogéneos es responsabilidad del runtime, no convención voluntaria del autor de cada tool.

## Modelo mental

- `PostToolUse` es runtime garantizado, no convención del autor de la tool: matchea por patrón y se aplica a TODAS las tools que matcheen.
- `updatedMCPToolOutput` reemplaza el output crudo; el modelo nunca ve el XML.
- Los mapas de traducción (`STATUS_MAP`) y esquemas viven en código recargable, en un solo lugar.
- `additionalContext` anexa metadatos auditables (origen legacy, timestamp de normalización) sin contaminar el payload limpio que consume el modelo.

## Patrón correcto

```python
STATUS_MAP = {"0xA1": "paid", "0xB2": "pending", "0xC3": "overdue"}

async def normalize_legacy(input, tool_use_id, ctx):
    raw = input["tool_response"]
    clean = {
        "order_id": raw.find("OrderId"),
        "status": STATUS_MAP.get(raw.find("StatusCode"), "unknown"),
        "amount": float(raw.find("Total")),
    }
    return {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "updatedMCPToolOutput": {"type": "text", "text": json.dumps(clean)},
            "additionalContext": "source=legacy_erp_xml; normalized=true",
        }
    }
```

## Anti-patrón

```python
# Cada tool decide por su cuenta si normaliza, via decorators @tool.
@tool
def get_order(id):
    raw = legacy_erp.fetch(id)
    return normalize(raw)  # frágil: depende de que TODO autor lo recuerde

@tool
def get_invoice(id):
    return legacy_erp.fetch(id)  # un handler nuevo OLVIDÓ normalizar -> envenena contexto
```

## Argumento de certificación

La normalización de outputs heterogéneos es responsabilidad del runtime vía `PostToolUse`, no convención de cada tool. Defiende: el hook matchea por patrón y garantiza la transformación para todas las tools; `updatedMCPToolOutput` impide que el XML crudo entre al historial; `additionalContext` sirve para metadatos auditables que el modelo no necesita ver. Quiz de referencia: C·B·B.

## Cuándo activar

- Una o más tools devuelven payloads heterogéneos o legacy (XML, códigos de estado opacos) que conviene canonizar.
- Se quiere una sola fuente de verdad para la transformación, robusta ante tools nuevas.
- El usuario menciona `PostToolUse`, `updatedMCPToolOutput`, normalización de output o payloads legacy.

## Skills relacionadas

- `katas-tool-result-defensive-extraction`
- `katas-hook-driven-control`
- `katas-headless-code-review`

## Evidence Requirements

- Cita el código del hook, el `STATUS_MAP` y la firma de `updatedMCPToolOutput` usados.
- Marca inferencias y supuestos explícitamente.

## Update-Safety Notes

- Los archivos de soporte generados son missing-only por defecto.
- Usa `--force` solo tras revisar diffs.
