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

## Contrato determinístico

Los assets bajo `assets/` definen un reporte JSON auditable con:

- `sources`: fuente, ubicación y fecha.
- `claims`: claim tipado con `source_ids` no vacío y `as_of`.
- `conflicts`: desacuerdos preservados con `resolution_policy=escalate`.
- `escalations`: cola humana por cada conflicto.
- `render`: flags que prueban source, fecha y marcador de conflicto visibles.
- `structural_tests`: flags que prueban que la invariante no depende de prosa.

## Validación

```bash
bash skills/provenance-engineering/scripts/check.sh
```

El check ejecuta fixtures válidos e inválidos para asegurar que no haya claims sin fuente, source ids desconocidos, conflictos promediados, escalaciones omitidas ni fechas ocultas.
