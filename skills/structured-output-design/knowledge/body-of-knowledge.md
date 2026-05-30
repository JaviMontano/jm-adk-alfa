<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Structured Output Design Body of Knowledge

## Canon

La salida estructurada de Claude se diseña como un **contrato de datos**, no como prosa parseada. El contrato vive en el `input_schema` de una tool y se hace cumplir con `tool_choice`. El consumidor lee `tool_use.input` (ya deserializado), nunca aplica `json.loads` sobre texto.

## Conceptos clave

- **Schema defensivo:** un JSON Schema que codifica lo que la fuente garantiza, no lo que se desea. `required` = presencia real; opcional = unión `["tipo", "null"]`.
- **Nullable union:** un campo opcional se modela como `["string", "null"]`. Ausente se representa con `null`, nunca con un default falso (`''`, `0`, `"N/A"`).
- **Válvula de escape en enums:** todo enum cerrado incluye `'other'` y un campo hermano `details` que captura el valor textual cuando no encaja. El catálogo evoluciona con evidencia en vez de descartar filas.
- **`tool_choice` forzado:** `{"type": "tool", "name": ...}` obliga al modelo a emitir esa estructura. Se usa solo cuando emitir el schema es la única acción válida; no cuando el modelo debe decidir entre varias herramientas.
- **Parseo tipado:** localizar el bloque `type == "tool_use"`, leer `.input`. Sin regex, sin code fences, sin `json.loads(text)`.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| `required` honesto | Cada `required` corresponde a presencia real en la fuente |
| Opcionales nullable | Sin defaults `''`/`0`/`"N/A"`; ausente = `null`/`unclear` |
| Enums con escape | Todo enum cerrado tiene `'other'`+`details` |
| `tool_choice` justificado | Forzado solo si no hay decisión de tool legítima |
| Parseo tipado | Consumidor lee `tool_use.input`, no prosa |
| Validación previa | Salida validada contra schema antes de aceptar; fallo → retry/escalada |

## Decisión de diseño: ¿forzar tool_choice?

- Una sola acción válida = emitir la estructura → **fuerza** `{"type": "tool", "name": ...}`.
- El modelo elige entre varias tools (p. ej. extraer vs escalar) → **no fuerces**; usa `auto` o `any`.
- Necesitas alguna tool pero no importa cuál → `{"type": "any"}`.

## Anti-patrón canónico

"Devuelve JSON" en prosa + `json.loads(text)`. Se rompe cuando el modelo añade prosa o un code fence; los defaults `''` ocultan ausencia real; el enum cerrado descarta cada caso imprevisto. Es la firma exacta que el guardian debe rechazar.

