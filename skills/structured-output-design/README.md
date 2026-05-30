<!--
generated-by: scripts/scaffold-skill.py
generated-for: structured-output-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# structured-output-design

## Resumen ejecutivo

Capacidad de ingeniería para forzar que Claude emita datos estructurados como un contrato verificable en vez de prosa parseada a mano. Se materializa en un JSON Schema defensivo (`required` reales, opcionales `nullable`, enums con válvula de escape `'other'`+`details`) cargado como `input_schema` de una tool, con `tool_choice` forzado cuando la única acción válida es emitir la estructura. El consumidor parsea desde `tool_use.input`, nunca desde texto.

## Triggers

- structured output design
- json schema output
- defensive schema
- forced tool_choice
- "el `json.loads` se rompe a veces"
- "un campo opcional ausente sale como cadena vacía"
- "el enum cerrado pierde casos reales"

## Allowed Tools

`Read`, `Grep`, `Glob`, `Bash` (read-only-first: inspeccionar definiciones de tools y schemas antes de proponer cambios).

## Quick Use

1. Inventaria los campos de la fuente: garantizados (`required`) vs ocasionales (opcionales `nullable`).
2. Define el schema como `input_schema` de la tool; añade `'other'`+`details` a cada enum cerrado.
3. Fuerza `tool_choice` solo si no hay decisión de tool legítima.
4. Parsea desde `tool_use.input`; valida contra el schema; enruta fallos a retry/escalada.

## Output Format

Markdown con resumen, evidencia, schema propuesto, patrón GOOD/ANTI, checklist y riesgos. Ver `SKILL.md` para el patrón completo, `prompts/` para prompts de producción y `evals/evals.json` para los casos de activación.
