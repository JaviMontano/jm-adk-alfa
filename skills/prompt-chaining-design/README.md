<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design

Capacidad de ingeniería para descomponer una tarea grande en una cadena de pases: un **pase local tipado** que procesa cada unidad aislada y emite un resumen contra schema, y un **pase de integración** que solo consume esos resúmenes (nunca los crudos). Entre ambos vive un **schema de transición** explícito con estado de error tipado por unidad. Reemplaza el mega-prompt saturado por map → reduce paralelizable y trazable.

## Triggers

- prompt chaining design
- multipass decomposition
- transition schema
- chained passes

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Invócala cuando el volumen de unidades excede lo que un single-pass procesa con calidad, las unidades son independientes y solo se integran al final. Construye en orden: unidad atómica → schema del pase local → schema de transición → pase de integración sobre resúmenes → justificación vs single-pass.

## Output Format

Markdown con summary, evidence, result, validation y risks. El artefacto técnico incluye los schemas tipados de cada pase y el contrato de transición.
