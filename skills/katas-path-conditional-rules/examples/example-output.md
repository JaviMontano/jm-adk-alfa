<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-path-conditional-rules
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se separaron las reglas del monorepo en universales y condicionales por glob. La seguridad queda siempre cargada; estilo/testing Python y Terraform se cargan solo al editar sus archivos. Editar un README ya no arrastra heurísticas de lenguaje.

## Evidence

- Kata 09 · Reglas condicionales por ruta (`docs/katas/katas-content.md`).
- `input_tokens` por turno comparados editando `README.md` vs `src/app/service.py`.

## Result

### Clasificación de reglas

| Regla | Clase | Glob de activación |
|---|---|---|
| `security.md` | universal | — |
| `python-style.md` | condicional | `src/**/*.py` |
| `python-testing.md` | condicional | `src/**/*.py` |
| `terraform.md` | condicional | `infra/**/*.tf` |

### CLAUDE.md resultante (GOOD)

```text
@rules/security.md   # universal, siempre cargada

## When editing src/**/*.py:
@rules/python-style.md
@rules/python-testing.md

## When editing infra/**/*.tf:
@rules/terraform.md
```

### CLAUDE.md anterior (ANTI)

```text
@rules/python-style.md
@rules/python-testing.md
@rules/terraform.md
@rules/security.md
# Todas cargan siempre, aunque solo edites el README.
```

### Ahorro estimado de tokens

Editar `README.md`: solo `security.md` (~120 tokens) en lugar de las cuatro reglas (~2000 tokens). Ahorro ~94% de la memoria de reglas en sesiones que no tocan código.

## Validation

- Cada regla clasificada como universal o condicional por glob.
- `security.md` siempre cargada; `python-style.md` NO se carga al editar el README.
- Globs sin solapes ambiguos; `src/**/*.py` e `infra/**/*.tf` cubren los tipos relevantes.
- Ahorro de tokens medido con `input_tokens` README vs `.py`.

## Risks and Limits

- Si una regla de seguridad se cuela en un bloque condicional, dejaría archivos sin cubrir: revisar antes de cerrar.
- Globs demasiado amplios pueden recargar reglas en archivos inesperados.
