---
name: provenance-engineering
version: 1.0.0
description: "Preservar provenance tipada con invariante no hay claim sin source y conflictos marcados y escalados, no promediados."
owner: "JM Labs"
triggers:
  - provenance engineering
  - claim source invariant
  - conflict marking
  - typed provenance
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Provenance Engineering

## Capacidad

Diseñar e implementar pipelines de extracción/síntesis donde cada claim transporta su provenance tipada y donde la invariante "no hay claim sin source" es estructural, no aspiracional. La capacidad cubre tres decisiones de ingeniería: (1) modelar cada afirmación como un objeto con `source[]` obligatorio (id, ubicación, fecha), (2) detectar y representar conflictos entre fuentes con `conflict=true` conservando ambas fuentes en lugar de promediarlas o elegir una en silencio, y (3) escalar los conflictos a revisión humana con la fecha visible, nunca resolverlos automáticamente. El resultado es un artefacto auditable donde un humano puede trazar cualquier dato hasta su origen y ver qué fuentes lo respaldan o lo contradicen.

## Cuándo usarla

- Construyes un pipeline que extrae datos de múltiples documentos (KYC, due diligence, research multi-fuente) y el output será usado para decidir, firmar o citar.
- Distintas fuentes pueden contradecirse (dos fechas, dos cifras, dos direcciones) y promediar o elegir una destruye información crítica.
- El consumidor del output es un humano que necesita auditar el origen de cada dato antes de actuar.
- Necesitas un test estructural que falle el build si aparece un claim sin source.

No la uses cuando el output es prosa exploratoria sin consecuencias de decisión, o cuando una sola fuente de verdad es indiscutible y no hay posibilidad de conflicto.

## Cómo construir

1. **Modela el claim tipado.** Define un tipo `Claim` con `value`, `source[]` no vacío y `as_of` (fecha). El `source[]` vacío debe ser inválido por construcción (tipo, schema o validación en el constructor), no por convención.
2. **Captura la provenance en extracción.** En cada extracción, adjunta `source_id`, ubicación dentro de la fuente (página, span, celda) y fecha del documento. Nunca dejes que un claim nazca sin esos campos.
3. **Detecta conflictos al fusionar.** Al consolidar claims sobre el mismo atributo desde varias fuentes, compara valores normalizados. Si difieren, marca `conflict=true` y conserva todas las fuentes; no colapses a un valor único.
4. **Escala, no resuelvas.** Enruta los claims con `conflict=true` a una cola de revisión humana con ambas fuentes y la fecha visible. El pipeline no decide cuál gana.
5. **Hazlo visible para el humano.** En el render, expón `source_id` y `as_of` junto a cada claim; los conflictos se muestran como tales, no enterrados.
6. **Blinda con un test estructural.** Agrega un test que recorra el output y falle si existe cualquier claim con `source[]` vacío o si un conflicto fue silenciosamente resuelto.

## Patrón correcto

```python
from dataclasses import dataclass
from datetime import date

@dataclass(frozen=True)
class Source:
    source_id: str
    locator: str   # page 4, cell B7, span 120-138
    as_of: date

@dataclass(frozen=True)
class Claim:
    attribute: str
    value: str
    sources: tuple[Source, ...]
    conflict: bool = False

    def __post_init__(self) -> None:
        if not self.sources:
            raise ValueError(f"claim '{self.attribute}' has no source")  # GOOD: invariant enforced

def merge(attribute: str, candidates: list[Claim]) -> Claim:
    values = {c.value for c in candidates}
    all_sources = tuple(s for c in candidates for s in c.sources)
    # GOOD: conflict is preserved with both sources, never averaged or silently picked
    return Claim(attribute, value=" | ".join(sorted(values)), sources=all_sources,
                 conflict=len(values) > 1)

def assert_provenance(claims: list[Claim]) -> None:
    for c in claims:
        assert c.sources, f"claim '{c.attribute}' lost its source"  # GOOD: structural test
```

## Anti-patrón

```python
# ANTI: prose summary with no source_id, no date, no conflict signal
def summarize(records: list[dict]) -> str:
    name = records[0]["name"]            # picks first source silently
    revenue = sum(r["revenue"] for r in records) / len(records)  # ANTI: averages a conflict
    return f"{name} reported revenue of {revenue}."  # no provenance, no as_of, conflict erased
```

Esto destruye la auditabilidad: el humano no puede saber de dónde salió el nombre, el conflicto de cifras quedó promediado en un número que ninguna fuente afirma, y no hay fecha. Un dato así no puede sostener una decisión.

## Checklist de validación

- ¿Cada claim transporta `source[]` no vacío (id + ubicación + fecha)?
- ¿Los conflictos están marcados con `conflict=true` y conservan todas las fuentes?
- ¿Los conflictos se escalan a humano en lugar de resolverse/promediarse automáticamente?
- ¿La fecha (`as_of`) es visible para el humano en el render?
- ¿Existe un test estructural que falle si aparece un claim sin source o un conflicto silenciado?

## Katas y skills relacionadas

- Kata 20.
- Relacionadas: `katas-provenance-preservation`.
