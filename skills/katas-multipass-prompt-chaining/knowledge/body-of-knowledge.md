<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining Body of Knowledge

## Canon

Kata 12 · Prompt Chaining Multi-Pass · escenario Multi-Agent Orchestration.

Cuando una tarea no cabe cognitivamente en un solo prompt, se descompone en pases secuenciales que se componen como una pipeline:

- **Pase 1 (local, paralelizable):** una invocación por unidad (archivo, sección, página). Salida tipada y compacta según un schema declarado (p. ej. `FileFindings`). Cada unidad se procesa aislada y no ve a las demás.
- **Pase 2 (integración):** consume únicamente las salidas tipadas del pase 1. Nunca ve las unidades crudas ni la totalidad sin filtrar. Emite el resultado final según su propio schema (p. ej. `AuditReport`).
- **Schemas de transición:** cada pase declara el schema de su salida; el siguiente pase consume exactamente ese schema. Esta es la pieza de diseño central de la kata.

## Conceptos clave

| Concepto | Definición |
|---|---|
| Pase local | Procesamiento independiente por unidad con salida tipada según schema; paralelizable vía subagentes (Kata 4). |
| Pase de integración | Combina solo los resúmenes tipados del pase 1; jamás re-ingiere las unidades crudas. |
| Schema de transición | Contrato tipado que conecta la salida de un pase con la entrada del siguiente. |
| Estado de error tipado | Campo por unidad que declara si el procesamiento de esa unidad tuvo éxito; sin él, la falla es silenciosa. |
| Candidatura a chaining | Decisión de usar multi-pass solo cuando la tarea no cabe holgadamente y el overhead de coordinación se justifica. |

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Aislamiento del pase 1 | Cada unidad se procesa sin ver a las demás; sin dependencias cruzadas. |
| Tipado de transición | Pase 1 y pase 2 declaran y consumen schemas explícitos. |
| Filtrado del pase 2 | El pase 2 solo recibe resúmenes tipados, nunca unidades crudas. |
| Estado de error por unidad | Existe `status`/`error` por unidad; el conteo de unidades válidas es explícito (no asume N). |
| Justificación del overhead | El chaining se usa solo si la tarea no cabe holgadamente en single-pass. |

## Anti-patrón canónico

```python
mega_prompt = "\n\n".join(open(f).read() for f in files)
create(messages=[{"role": "user", "content": f"Audita todo:\n{mega_prompt}"}])
```

Concatenar todas las unidades crudas en un solo prompt satura la atención del modelo (Kata 11), no paraleliza, pierde detalles y alucina relaciones entre archivos. El resumen resultante parece correcto pero no es auditable.

## Quiz oficial (clave B·A·A)

- **P1 (B):** chaining con schemas tipados; el pase 2 nunca ve los originales, solo los resúmenes.
- **P2 (A):** NO conviene cuando la tarea cabe holgadamente y el overhead de coordinación supera el beneficio.
- **P3 (A):** sin estado de error tipado por unidad, el pase 2 cree que tiene N-1 unidades válidas como si fueran N: falla silenciosa.

## Katas relacionadas

- Kata 4 · subagentes para paralelizar el pase 1.
- Kata 11 · cada pase respeta el límite de contexto.
- Kata 20 · preservación de provenance en la agregación.
