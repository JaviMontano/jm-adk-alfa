<!--
generated-by: scripts/scaffold-skill.py
generated-for: provenance-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Provenance Engineering Primary Prompt

## Objective

Construir o revisar un pipeline de extracción/síntesis multi-fuente donde cada claim transporta provenance tipada bajo la invariante "no hay claim sin source", y donde los conflictos entre fuentes se marcan y escalan, nunca se promedian.

## Required Inputs

- Fuentes a procesar (documentos, su tipo y fecha).
- Atributos a extraer y consolidar.
- Consumidor del output (humano que decide/firma/cita) y nivel de auditabilidad requerido.
- Definición de done: invariante enforzada, conflictos visibles, test estructural en verde.

## Process

1. Define el tipo `Claim` con `value`, `source[]` no vacío y `as_of`; hazlo inválido por construcción si `source[]` está vacío.
2. Instrumenta la extracción para capturar `source_id`, ubicación (página/span/celda) y fecha en cada claim.
3. Al fusionar claims del mismo atributo, marca `conflict=true` y conserva todas las fuentes cuando los valores difieren.
4. Enruta los conflictos a una cola de revisión humana con ambas fuentes y `as_of` visibles; no los resuelvas.
5. Renderiza exponiendo `source_id` y `as_of` junto a cada claim.
6. Agrega un test estructural que falle si hay un claim sin source o un conflicto silenciado.

## Output

Devuelve el deliverable en este shape: Markdown con summary, evidencia (claims con `source[]` y `as_of`), resultado, validación (checklist completo) y riesgos. El código en inglés; la prosa en español.
