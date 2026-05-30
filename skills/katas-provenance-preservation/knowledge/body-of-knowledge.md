<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-provenance-preservation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Provenance Preservation Body of Knowledge

## Canon

Kata 20 · Preservación de Provenance. Cada afirmación factual extraída de fuentes mantiene un mapeo tipado a su origen: `claim, source_id, source_name, publication_date`. Escenarios: Multi-Agent Orchestration, Structured Extraction.

### Conceptos clave

- **Invariante de schema.** "No hay claim sin source" no es una recomendación: es una propiedad del schema del output. Un claim sin `sources[]` no válido no debe existir en el resultado.
- **Política de conflictos.** Si dos fuentes contradicen un dato, se registran ambas bajo `conflict=true` con `needs_human_review=true`. No se promedia, no se elige. La resolución se escala a humano vía Kata 16.
- **La fecha informa, no decide.** `publication_date` debe estar presente para que el humano juzgue. La fuente más reciente no siempre gana (un reporte anual auditado puede pesar más que un deck de inversores posterior).
- **El punto de fuga es la agregación.** Tras subagentes paralelos (Kata 4), el "quién dijo qué" se pierde si la fuente no es campo obligatorio en el contrato de agregación.
- **Verificación numérica adyacente (Kata 15).** Provenance dice de dónde viene un número; la verificación numérica confirma que el número es correcto. Son complementarias.

### Señales de calidad

| Señal | Objetivo |
|---|---|
| Cobertura de provenance | Cada `claim` del output tiene `sources[]` no vacío con `source_id` existente |
| Conflictos explícitos | Toda contradicción entre fuentes está marcada `conflict=true` y escalada, nunca silenciada |
| Fecha presente | Cada fuente lleva `publication_date` para que el humano pueda juzgar |
| Auditabilidad | El output es verificable claim por claim, no prosa libre |

### Anti-patrón canónico

```python
summary = "La empresa tiene ARR de 12M USD y 462 empleados..."
```

Prosa libre sin `source_id`, sin fecha y sin conflicto marcado: se ve correcta, no es auditable, y puede alucinar el dato de headcount (462) ocultando que doc-A decía 450.

## Open Knowledge

- Añadir referencias específicas de proyecto a medida que se estabilicen.
