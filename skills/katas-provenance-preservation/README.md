<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation

Kata 20 · Preservación de Provenance. Provenance tipada: no hay claim sin source; los conflictos entre fuentes se marcan con `conflict=true` y se escalan a humano, nunca se promedian ni se eligen en silencio.

## Resumen ejecutivo

Cuando se agregan hechos de muchas fuentes (especialmente tras subagentes paralelos), cada afirmación factual debe mantener un mapeo tipado a su origen: `claim, source_id, source_name, publication_date`. Esto convierte un resumen no auditable en un artefacto verificable claim por claim, y evita que alucinaciones en prosa libre pasen desapercibidas. Escenarios: Multi-Agent Orchestration, Structured Extraction.

## Triggers

- provenance preservation
- claim source mapping
- conflict flag
- source provenance

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando el output sea un reporte factual derivado de varias fuentes y deba ser auditable. Para cada claim emite un objeto con `sources[]` no vacío (cada uno con `source_id`, `name`, `date`). Si dos fuentes contradicen un mismo dato, registra ambas, marca `conflict=true`, fija `needs_human_review=true` y escala vía Kata 16.

## Output Format

Markdown o JSON con: lista de `claims[]`, cada uno con `sources[]` tipadas, bandera `conflict`, y nota de validación estructural (cada claim tiene fuente).
