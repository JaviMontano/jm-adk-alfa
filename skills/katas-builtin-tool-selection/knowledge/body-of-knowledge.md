<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-builtin-tool-selection
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Builtin Tool Selection Body of Knowledge

## Canon

Kata 23. Selección de built-in tools de Claude Code. Cada tool tiene un uso primario y un failure mode:

| Tool | Uso primario | Failure mode / nota |
|---|---|---|
| `Grep` | Buscar contenido por regex | Mira contenido, no nombres de path |
| `Glob` | Buscar paths por patrón de nombre | No inspecciona contenido |
| `Read` | Cargar un archivo en contexto | `Read` masivo del repo quema tokens |
| `Edit` | Modificación dirigida sobre anchor único | Anchor no único o inexistente → falla |
| `Write` | Sobrescribir archivo completo | Reemplaza todo; sin diff dirigido |
| `Bash` | Ejecutar shell | Efectos colaterales fuera del editor |

### Estrategia canónica

`Grep` primero (encontrar entry points por contenido) → `Read` selectivo (seguir imports) → `Edit`/`Write` puntual. Fallback cuando `Edit` falla por anchor ambiguo: `Read` entero + `Write` completo. La regla dura: nunca leer todo el repo upfront.

### Criterio de tool por intención

- Listar archivos por nombre/patrón (p. ej. `**/*.test.tsx`) → `Glob`.
- Encontrar dónde se define o usa un símbolo → `Grep`.
- Cambiar una línea concreta → `Edit` con anchor único; si el anchor matchea varias líneas, ampliarlo con contexto suficiente o caer a `Write`.
- Rastrear un flujo (auth, login, session) → `Grep` de los términos → `Read` selectivo → seguir imports.

## Quality Signals

| Signal | Target |
|---|---|
| Tool fit | El tool elegido coincide con la intención (contenido vs path vs mod) |
| Token economy | No hay `Read` masivo upfront; la exploración es incremental |
| Edit safety | Los anchors de `Edit` son únicos; fallback `Read` + `Write` definido |
| Evidence coverage | Las afirmaciones se apoyan en matches reales o se marcan como supuestos |
| Offline contract | `assets/` y `scripts/check.sh` validan tool-fit, economía de lectura, anchor y fallback |

## Anti-patrón canónico

```python
all_files = glob("**/*")
for f in all_files:
    read(f)  # 200k tokens cargados sin necesidad

edit(old_text="if amount", ...)  # múltiples líneas matchean → falla
```

Dos errores combinados: cargar el repositorio entero upfront y editar con un anchor ambiguo.

## Deterministic Validation

- Aceptar `Grep` sólo para búsqueda por contenido; aceptar `Glob` sólo para búsqueda por path.
- Exigir `search_before_read=true` cuando el target es desconocido.
- Rechazar `read_plan.mass_read_upfront=true`.
- Para `Edit`, exigir `anchor.unique_match_count == 1` y fallback declarado.
- Para `Write`, exigir trigger `ambiguous-anchor`, lectura completa previa y razón explícita.
- Rechazar reportes que requieren red, random o contienen `read_all_files`, `repo_wide_read`, `ambiguous_edit_anchor` o `tool_mismatch` como patrón aceptado.

## Open Knowledge

- Quiz de referencia: C·C·B (P1 `Glob` con `**/*.test.tsx`; P2 ampliar anchor + `Write` como fallback explícito; P3 `Grep` `authenticate`/`login`/`session` → `Read` selectivo → seguir imports).
