<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Estrategia `Grep` → `Read` → `Edit`: localicé `processRefund` por contenido, leí solo ese archivo y apliqué la modificación con un anchor único.

## Evidence

GOOD (patrón correcto):

```python
matches = grep(pattern="processRefund\\(", glob="**/*.py")
content = read(matches[0].path)
edit(
    path=matches[0].path,
    old_text="if amount > 1000:",
    new_text="if amount > MAX_REFUND:",
)
```

ANTI (lo que se evita):

```python
all_files = glob("**/*")
for f in all_files:
    read(f)  # 200k tokens cargados sin necesidad

edit(old_text="if amount", ...)  # múltiples líneas matchean → falla
```

## Result

`Edit` aplicado sobre el único archivo que define `processRefund`, reemplazando `if amount > 1000:` por `if amount > MAX_REFUND:`.

## Validation

- Tool elegido coincide con la intención: `Grep` para contenido, `Read` selectivo, `Edit` puntual.
- Sin `Read` masivo upfront: no se cargó el repositorio entero.
- Anchor de `Edit` único (`if amount > 1000:`), no el ambiguo `if amount`.
- Fallback definido: si el anchor no fuese único, `Read` entero + `Write` completo.

## Risks and Limits

- Si `processRefund` apareciera en más de un archivo, validar el `matches[0]` correcto antes de editar.
- Confirmar que `MAX_REFUND` está importada/definida en el módulo destino.
