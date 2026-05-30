<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Tool Description Quality Primary Prompt

## Objective

Convertir un conjunto de tools con descripciones ambiguas en contratos de selección no solapados, para que el modelo enrute al tool correcto en cada turno.

## Required Inputs

- La definición actual de los tools (name + description + input_schema).
- El system prompt vigente (para detectar keywords que sesgan el routing).
- El síntoma observado (qué turnos enrutan mal y a qué tool).
- Definition of done: misroute por debajo del umbral acordado.

## Process

1. **Discover** — Inspeccionar la toolset; localizar pares con verbo idéntico, sustantivos casi sinónimos y sin frontera.
2. **Analyze** — Decidir por tool: ¿rename (el nombre confunde), split (acumula modos) o frontera (le falta el "usa X en lugar de Y")? Revisar el system prompt por sesgo de keywords.
3. **Execute** — Reescribir cada descripción con input format + ejemplo de query + frontera explícita recíproca. Aplicar rename/split donde corresponda.
4. **Validate** — Confirmar que no queda contrato solapado y que las fronteras son recíprocas.

## Output

Markdown con summary, evidence, result (el JSON de tools reescrito), validation, y risks.
