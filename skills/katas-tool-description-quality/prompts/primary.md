# Katas Tool Description Quality Primary Prompt

## Objective

Convertir tools ambiguos en contratos de seleccion no solapados.

## Required Inputs

- Definitions actuales: `name`, `description`, `input_schema`.
- System prompt vigente, si existe.
- Sintoma observado de misroute.
- Umbral aceptado de misroute.

## Process

1. Descubrir pares con contrato solapado.
2. Clasificar accion: `keep`, `rename`, `split` o `boundary_only`.
3. Reescribir descripciones con input format, ejemplo de query y frontera reciproca.
4. Validar contra `assets/tool-description-contract.json` y script offline cuando se emite JSON.

## Output

Markdown o JSON con evidencia, tools reescritos, validacion y riesgos residuales.
