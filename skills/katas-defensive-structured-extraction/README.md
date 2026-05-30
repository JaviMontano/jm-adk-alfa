<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-defensive-structured-extraction
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Defensive Structured Extraction

Kata 05 del kit JM-ADK · Extracción estructurada defensiva con JSON Schema.

## Resumen ejecutivo

Fuerza `tool_choice` con un JSON Schema que declara los `required` reales, modela opcionales como union nullable y define enums con válvula de escape (`'other'`, `'unclear'`) más un campo `details`. El modelo nunca devuelve prosa: invoca siempre la herramienta de extracción. Así se eliminan las alucinaciones silenciosas que aparecen al pedir "devuélveme JSON" en lenguaje natural y parsear con `json.loads(resp.text)`.

## Triggers

- defensive extraction
- json schema extraction
- forced tool_choice
- nullable union

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

1. Define un tool con `input_schema` cuyos `required` sean solo los campos siempre presentes en la fuente.
2. Modela cada opcional como `{"type":["string","null"]}` y cada enum con `'other'`/`'unclear'` + campo `details`.
3. Llama `create(tools=[EXTRACT_TOOL], tool_choice={"type":"tool","name":"..."})`.
4. Valida que no haya defaults `''` ni valores fuera de dominio antes de pasar el JSON aguas abajo.

## Output Format

Markdown con summary, evidence, result, validation y risks; el artefacto central es el tool-use block con el JSON conforme al schema.
