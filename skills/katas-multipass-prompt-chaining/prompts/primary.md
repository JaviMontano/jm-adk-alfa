<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining Primary Prompt

## Objective

Aplicar Kata 12 (Prompt Chaining Multi-Pass) a una tarea que no cabe en un solo prompt: descomponerla en un pase local tipado por unidad y un pase de integración que solo ve los resúmenes.

## Required Inputs

- Conjunto de unidades a procesar (archivos, secciones, páginas) y cómo enumerarlas.
- Schema de salida del pase 1 por unidad (incluyendo estado de error tipado).
- Schema de salida del pase 2 de integración.
- Definición de done y criterios de aceptación.

## Process

1. **Candidatura.** Confirmar que la tarea no cabe holgadamente en single-pass; si cabe, no encadenar.
2. **Pase 1 (local).** Por cada unidad, invocar de forma aislada y emitir salida tipada según el schema, con `status`/`error` por unidad. Paralelizar vía subagentes (Kata 4) si aplica.
3. **Pase 2 (integración).** Consumir solo los resúmenes tipados del pase 1, nunca las unidades crudas. Contar las unidades válidas a partir del estado de error. Emitir el resultado según el schema de integración.
4. **Validate.** Verificar aislamiento del pase 1, tipado de transición, filtrado del pase 2 y conteo correcto de unidades válidas.

## Anti-pattern a rechazar

```python
mega_prompt = "\n\n".join(open(f).read() for f in files)
create(messages=[{"role": "user", "content": f"Audita todo:\n{mega_prompt}"}])
```

## Output

Devolver el entregable como Markdown con summary, evidence, result (separando pase 1 y pase 2), validation y risks.
