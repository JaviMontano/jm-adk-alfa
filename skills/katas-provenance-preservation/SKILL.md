---
name: katas-provenance-preservation
version: 1.0.0
description: "Provenance tipada: no hay claim sin source; conflictos marcados con conflict true y escalados, nunca promediados."
owner: "JM Labs"
triggers:
  - provenance preservation
  - claim source mapping
  - conflict flag
  - source provenance
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Katas Provenance Preservation

## Qué es

Cada afirmación factual (`claim`) extraída de fuentes mantiene un mapeo tipado a su origen: `claim, source_id, source_name, publication_date`. Los conflictos entre fuentes NO se resuelven en silencio: se marcan con `conflict=true` y se enrutan a un humano. La provenance no es un metadato opcional sino parte del schema del output: si un claim no puede señalar su fuente, no debe existir en el resultado.

## Por qué importa (falla que evita)

Tras agregar contenido de muchas fuentes vía subagentes (Kata 4), perder el hilo de "quién dijo qué" hace imposible auditar el resultado. Los resúmenes en prosa libre se ven correctos y alucinan sin que se note: el lector no tiene forma de distinguir un dato verificado de uno inventado. La provenance tipada es la única defensa, porque convierte "confía en mi resumen" en "verifica cada claim contra su fuente".

## Modelo mental

- No hay claim sin source: es un invariante de schema, no una buena práctica.
- Si dos fuentes contradicen, se registran ambas bajo `conflict=true`; no se promedia, no se elige.
- La fecha de publicación importa pero no decide: el humano necesita verla para juzgar (la fuente más reciente no siempre gana).
- El conflicto se escala a humano (vía Kata 16), no se resuelve por heurística del modelo.
- La agregación tras subagentes paralelos (Kata 4) es el punto donde la provenance se pierde si no es un campo obligatorio del schema.

## Patrón correcto

```python
claims = [
    {
        "claim": "ARR Q3 2025 = 12M USD",
        "sources": [
            {"id": "doc-A", "name": "Annual Report", "date": "2025-12-01"},
            {"id": "doc-B", "name": "Investor Deck", "date": "2025-09-15"},
        ],
        "conflict": False,
    },
    {
        "claim": "Headcount end-2025",
        "sources": [
            {"id": "doc-A", "value": "450"},
            {"id": "doc-C", "value": "462"},
        ],
        "conflict": True,
        "needs_human_review": True,
    },
]
```

## Anti-patrón

```python
summary = "La empresa tiene ARR de 12M USD y 462 empleados..."
# sin source_id, sin fecha, sin conflicto marcado: provenance perdida
```

## Argumento de certificación

- Enunciar el invariante "no hay claim sin source" como propiedad del schema, no como recomendación.
- Describir la política de conflictos: registrar ambas posturas, no promediar ni elegir, escalar vía Kata 16.
- Conectar con Kata 4 (agregación tras subagentes paralelos) y Kata 15 (verificación numérica).
- Demostrar un test estructural que asserta que cada `claim` del output tiene un campo `sources[]` no vacío con `source_id` existente.

## Cuándo activar

- Extracción estructurada que agrega datos de múltiples documentos o fuentes.
- Salidas de orquestación multi-agente donde varios subagentes aportan hechos.
- Cualquier reporte factual que deba ser auditable claim por claim.
- Cuando dos fuentes pueden contradecirse y la respuesta debe preservar ambas.

## Skills relacionadas

- `katas-parallel-subagent-aggregation`
- `katas-numeric-verification`
- `katas-human-escalation`
