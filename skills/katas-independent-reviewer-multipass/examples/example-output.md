<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-independent-reviewer-multipass
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Resumen

Se rechaza el self-review y el quorum 2-de-3. El PR de 14 archivos se revisa con reviewers independientes en sesión limpia: Pass A per-file y Pass B cross-file.

## Patrón aplicado (GOOD)

```python
def review_pr(client, files):
    per_file = [
        review_file_independent(client, path, content)  # sesión NUEVA por archivo
        for path, content in files.items()
    ]
    summary = json.dumps(per_file)
    return create(
        system="Detecta interacciones cross-file y duplicados de findings.",
        messages=[summary],
    )
```

## Pass A · Findings per-file

- `payments/charge.py:42` — null deref si `amount` es None (error).
- `payments/refund.py:18` — clave de idempotencia no validada (warning). Reportado por un solo reviewer; se preserva (no se descarta por minoría).

## Pass B · Findings cross-file

- `charge.py` y `ledger.py` asumen unidades distintas (centavos vs unidades): contrato roto entre módulos.

## Validación

- [x] Reviewer en sesión limpia (no vio la generación).
- [x] Pass A y Pass B ejecutados por separado.
- [x] Sin quorum N-de-M; finding de minoría preservado.
