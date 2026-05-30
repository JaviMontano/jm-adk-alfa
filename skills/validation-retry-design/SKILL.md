---
name: validation-retry-design
version: 1.0.0
description: "Disenar loop de validacion y retry con error feedback especifico, distinguiendo recuperable de no recuperable, con tope y escalada."
owner: "JM Labs"
triggers:
  - validation retry design
  - error feedback loop
  - recoverable vs not
  - retry budget
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
---

# Validation Retry Design

## Capacidad

Capacidad de ingenieria para construir un loop `extract -> validate -> retry-with-error-feedback` que no reintenta a ciegas. Cuando un paso del agente produce una salida que falla la validacion, el loop reinyecta el **error especifico** (no el prompt original sin cambios) para que el siguiente intento corrija exactamente lo que rompio. El diseno distingue fallas **recuperables** (formato invalido, JSON malformado, campo fuera de rango) de **no recuperables** (dato ausente en la fuente, ambiguedad irresoluble), aplica un tope de reintentos (max 2-3) y, al agotarlo, **escala** con la cadena completa de errores en vez de aceptar una salida fallida en silencio.

## Cuando usarla

- Un agente o pipeline produce salida estructurada (JSON, schema, formato fijo) que a veces sale invalida.
- Necesitas que un reintento sea informado: el modelo debe saber por que fallo el intento previo.
- Hay que separar lo que se puede arreglar reintentando de lo que nunca se arreglara reintentando (falta el dato).
- Quieres acotar el costo: un presupuesto de reintentos en vez de bucles infinitos.
- Necesitas una ruta de escalada legible cuando el loop se rinde.

## Como construir

1. **Define el validador primero.** Escribe la funcion que decide pass/fail y que **devuelve un error especifico y accionable**, no un booleano pelado. El error es el insumo del retry.
2. **Clasifica el modo de falla.** En el validador marca cada error como `recoverable` (formato, parseo, rango) o `not_recoverable` (dato ausente, contradiccion en la fuente). Solo lo recuperable reintenta.
3. **Construye el feedback de retry.** Arma el prompt del siguiente intento incluyendo: salida previa + error exacto + instruccion de correccion. Nunca reenvies el prompt original intacto.
4. **Pon un tope.** Fija `max_retries` (2-3). Lleva un contador y la cadena de errores acumulada.
5. **Detecta patron sistematico.** Si el mismo error reaparece en cada intento, no es ruido: es un defecto estructural (prompt, schema o fuente). Rompe el loop y reporta el fix estructural en vez de gastar reintentos.
6. **Escala al agotar.** Al llegar al tope o ante una falla no recuperable, retorna estado de escalada con la cadena de errores completa y el ultimo output, para revision humana o un agente superior.

## Patron correcto

```python
# GOOD: retry informado, modo de falla clasificado, tope y escalada
def run_with_retry(task, max_retries=3):
    errors = []
    prev_output = None
    for attempt in range(max_retries):
        prompt = build_prompt(task, prev_output, errors[-1] if errors else None)
        output = model.run(prompt)
        verdict = validate(output)  # returns {"ok", "error", "recoverable"}
        if verdict["ok"]:
            return {"status": "ok", "output": output, "attempts": attempt + 1}
        if not verdict["recoverable"]:
            return escalate(reason="not_recoverable", errors=errors + [verdict["error"]])
        errors.append(verdict["error"])
        prev_output = output
        if is_systematic(errors):  # same error repeating -> structural defect
            return escalate(reason="systematic", errors=errors, fix_hint="schema/prompt")
    return escalate(reason="budget_exhausted", errors=errors, last_output=prev_output)


def build_prompt(task, prev_output, last_error):
    if prev_output is None:
        return task.base_prompt
    # reinject the SPECIFIC error, not the original prompt unchanged
    return (
        f"{task.base_prompt}\n\n"
        f"Your previous output failed validation: {last_error}\n"
        f"Previous output:\n{prev_output}\n"
        f"Fix only what failed; keep everything else."
    )
```

## Anti-patron

```python
# ANTI: reintento ciego + falla silenciosa
def run_bad(task, max_retries=3):
    for _ in range(max_retries):
        output = model.run(task.base_prompt)   # same prompt every time, no feedback
        if validate_bool(output):              # boolean only, no error reason
            return output
    return output  # accept the last failed output silently, no escalation
```

Por que falla: reenviar el prompt original sin el error hace que el modelo repita el mismo fallo; un validador booleano no tiene con que informar el retry; y devolver la ultima salida fallida sin escalar oculta el problema aguas abajo.

## Checklist de validacion

- [ ] El feedback del retry es el **error especifico** del intento previo, no el prompt original sin cambios.
- [ ] El validador devuelve causa accionable, no solo `true/false`.
- [ ] Se distingue recuperable (reintenta) de no recuperable (escala de inmediato).
- [ ] Hay tope de reintentos (max 2-3) con contador y cadena de errores.
- [ ] Se detecta patron sistematico para disparar fix estructural en vez de gastar reintentos.
- [ ] Al agotar reintentos hay escalada con la cadena completa de errores; nunca se acepta salida fallida en silencio.

## Katas y skills relacionadas

- Kata: `katas-26`
- Relacionada: `katas-validation-retry-feedback`
- Vecinas de diseno: `independent-review-design`, `workflow-forge`
