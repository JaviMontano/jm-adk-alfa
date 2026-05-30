<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Loop `extract -> validate -> retry-with-error-feedback` con validador accionable, clasificacion recuperable/no recuperable, tope de 3 y escalada con cadena de errores.

## Patron correcto (GOOD)

```python
def validate_invoice(output):
    try:
        data = json.loads(output)
    except json.JSONDecodeError as e:
        return {"ok": False, "error": f"Malformed JSON: {e}", "recoverable": True}
    if not isinstance(data.get("total"), (int, float)):
        return {"ok": False, "error": "Field 'total' must be a number, not a string with a symbol.", "recoverable": True}
    if not data.get("currency"):
        return {"ok": False, "error": "Field 'currency' is absent in the source invoice.", "recoverable": False}
    return {"ok": True, "error": None, "recoverable": True}


def extract_invoice(task, max_retries=3):
    errors, prev = [], None
    for attempt in range(max_retries):
        prompt = task.base_prompt if prev is None else (
            f"{task.base_prompt}\n\nPrevious output failed: {errors[-1]}\n"
            f"Previous output:\n{prev}\nFix only what failed."
        )
        out = model.run(prompt)
        v = validate_invoice(out)
        if v["ok"]:
            return {"status": "ok", "output": out, "attempts": attempt + 1}
        if not v["recoverable"]:
            return escalate("not_recoverable", errors + [v["error"]], out)
        errors.append(v["error"]); prev = out
    return escalate("budget_exhausted", errors, prev)
```

## Anti-patron (ANTI)

```python
def extract_invoice_bad(task, max_retries=3):
    for _ in range(max_retries):
        out = model.run(task.base_prompt)   # same prompt, no error feedback
        if is_valid(out):                    # boolean only
            return out
    return out  # silent failure, no escalation
```

## Validacion (checklist)

- [x] Feedback = error especifico previo, no prompt original
- [x] Validador con causa accionable (`error`)
- [x] `currency` ausente = no recuperable (escala); JSON / `total` = recuperable (reintenta)
- [x] Tope 3 con cadena de errores
- [x] Escalada explicita con cadena de errores y ultimo output
- [x] Sin salida fallida silenciosa

## Riesgos y limites

- Asume que el validador puede determinar de forma fiable cuando un campo es realmente irrecuperable vs solo mal formateado.
