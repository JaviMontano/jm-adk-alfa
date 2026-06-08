---
name: katas-validation-retry-feedback
version: 1.0.0
description: "Validacion y retry con error feedback especifico; distinguir recuperable de no recuperable; max 2-3 intentos y luego escalar."
owner: "JM Labs"
triggers:
  - validation retry
  - error feedback loop
  - retry with feedback
  - recoverable error
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Kata 26 · Validación y Retry con Error Feedback

## Qué es

Cuando una extracción tipada falla la validación (Pydantic / JSON Schema), no se reintenta a ciegas: se hace **retry-with-error-feedback**. La nueva llamada incluye el documento original, la extracción que falló y el error específico que produjo la validación, con la instrucción de corregir **solo** lo que el error señala. Se permiten máximo 2-3 intentos. La distinción clave es entre errores **recuperables** (formato, tipo, campo mal estructurado) y **no recuperables** (el dato simplemente no existe en la fuente).

## Por qué importa (falla que evita)

- Reintentar con el mismo prompt, sin feedback, es puro ruido: el modelo no sabe qué corregir y repite el mismo error.
- Aceptar una salida que falló validación en silencio rompe los contratos downstream que dependen del schema.
- Reintentar cuando el dato no existe en la fuente garantiza una alucinación: el modelo inventará un valor para satisfacer el schema.

## Modelo mental

- Loop: `extract → validate → (si error) extract+feedback → validate`.
- Máximo 2-3 intentos; el feedback debe ser el error específico, no un mensaje genérico.
- Tras N intentos sin éxito: marcar `needs_human_review` con la cadena de errores acumulados.
- Error recuperable (formato) y error no recuperable (información ausente en la fuente) son ramas distintas del flujo.
- Si el 80% de los fallos es el mismo error sistemático, el fix no es subir `max_retries`: es ajustar el schema/prompt o normalizar en post-process.

## Contrato determinístico

Usa los assets de `assets/` como contrato de salida antes de certificar la kata:

- `assets/validation-retry-contract.json`: campos JSON obligatorios y decisiones Guardian permitidas.
- `assets/error-classification-policy.json`: errores recuperables, no recuperables y reglas de retry.
- `assets/feedback-specificity-policy.json`: señales mínimas para considerar específico un feedback de retry.
- `assets/retry-limit-policy.json`: cap total de 2-3 intentos y reglas de escalada.
- `assets/evidence-policy.json`: evidencia mínima aceptada para validar el reporte.

Cuando el entregable sea JSON, valida offline con `scripts/validate_validation_retry_feedback.py`. Para la smoke determinística completa ejecuta `scripts/check.sh`, que acepta fixtures válidos y rechaza mutaciones inválidas.

## Patrón correcto

```python
def extract_with_retry(client, doc, schema, max_retries=2):
    last_error = None
    extraction = None
    for attempt in range(max_retries + 1):
        feedback = (
            f"Intento previo falló: {last_error}\n"
            f"Output previo: {extraction}\n"
            "Corrige SOLO lo que el error señala."
        ) if last_error else ""
        resp = client.messages.create(
            tools=[schema],
            tool_choice={"type": "tool", "name": schema["name"]},
            messages=[{"role": "user", "content": doc + feedback}],
        )
        extraction = resp.tool_use.input
        try:
            validate(extraction, schema)
            return {**extraction, "attempts": attempt + 1}
        except ValidationError as e:
            last_error = str(e)
    return {**(extraction or {}), "needs_human_review": True, "error_chain": last_error}
```

## Anti-patrón

```python
for _ in range(5):
    ext = extract(doc)
    try:
        validate(ext)
        return ext
    except Exception:
        continue  # mismo prompt, sin feedback: ruido puro
# ...y aceptar una salida fallida en silencio downstream
```

Mismo prompt cinco veces sin feedback específico, más aceptar la salida fallida sin marcarla.

## Argumento de certificación

- Distinguir error recuperable (formato) de no recuperable (dato ausente en la fuente).
- Describir el loop con feedback específico (error real, no mensaje genérico).
- Identificar patrones sistemáticos para un fix estructural en lugar de subir retries.
- Escalar con la cadena de errores cuando `max_retries` se agota (`needs_human_review`).
- Probar que ningún intento supera el cap total de 2-3 intentos ni reintenta un error marcado como no recuperable.

## Cuándo activar

- Una extracción tipada (Pydantic / JSON Schema) falla validación y hay que decidir el retry.
- Escenarios CI/CD y Structured Extraction donde el contrato downstream exige salida válida.
- Cuando aparece un loop de reintentos sin feedback o se acepta salida inválida en silencio.

## Skills relacionadas

- `katas-provenance-preservation`
- `katas-confidence-stratified-sampling`
- `katas-false-positive-criteria`
- `katas-multipass-prompt-chaining`
