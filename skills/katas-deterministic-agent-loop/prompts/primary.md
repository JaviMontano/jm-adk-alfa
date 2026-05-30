<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-deterministic-agent-loop
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Deterministic Agent Loop Primary Prompt

## Objective

Implementar o corregir un bucle agéntico de producción para que el control de continuación/parada dependa SOLO del campo estructurado `stop_reason`, nunca de la prosa del modelo.

## Required Inputs

- El código del bucle agéntico actual (o el objetivo del bucle si es nuevo).
- El SDK/cliente usado para llamar a la API (`create(...)`).
- El conjunto de herramientas que despacha el bucle.
- Política de budget deseada (límite de iteraciones).

## Process

1. Localiza la condición de halt actual. Si decide por texto (`"task complete"`, `"done"`, `"listo"`), márcala como anti-patrón.
2. Reescribe el bucle para enrutar por `stop_reason`:
   - `tool_use` → despacha la herramienta, reinyecta `tool_result` como `role=user`, continúa.
   - `end_turn` → finaliza.
   - cualquier otro valor → `raise UnhandledStop(resp.stop_reason)`.
3. Añade un budget configurable (`max_iterations`) que eleve `BudgetExceeded`.
4. Verifica que `max_tokens` y `pause_turn` no se traguen silenciosamente.

## Output

Devuelve el bucle corregido más una nota de validación que confirme: enrutamiento por `stop_reason`, manejo explícito de stops inesperados y presencia del budget. Markdown con resumen, evidencia, resultado, validación y riesgos.
