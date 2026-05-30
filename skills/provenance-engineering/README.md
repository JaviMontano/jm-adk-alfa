<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering

Capacidad de ingeniería para construir pipelines donde cada claim transporta provenance tipada bajo la invariante "no hay claim sin source", y donde los conflictos entre fuentes se marcan y escalan a humano, nunca se promedian ni se resuelven en silencio.

## Resumen ejecutivo

Cuando un output se usa para decidir, firmar o citar, cada dato debe ser trazable hasta su fuente y cada contradicción entre fuentes debe quedar visible. Esta skill encapsula el cómo: modelar `Claim` con `source[]` obligatorio y `as_of`, detectar conflictos al fusionar, escalarlos conservando ambas fuentes, y blindar todo con un test estructural que falle si aparece un claim sin source.

## Triggers

- provenance engineering
- claim source invariant
- conflict marking
- typed provenance

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Úsala cuando diseñes o revises un pipeline de extracción/síntesis multi-fuente cuyo output sostiene decisiones. Exige: tipo `Claim`, captura de provenance en extracción, política de conflictos (marcar y escalar, no promediar) y un test estructural de invariante.

## Output Format

Markdown con summary, evidencia (claims con `source[]` y `as_of`), resultado, validación (checklist) y riesgos.
