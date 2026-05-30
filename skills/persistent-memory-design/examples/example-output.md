<!--
generated-by: scripts/scaffold-skill.py
generated-for: persistent-memory-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

Se diseña un scratchpad persistente en `.agent/scratchpad.md` con esquema fijo (Hypotheses / Decisions / Findings / Open) que guarda solo conclusiones validadas de la auditoría PII, sobrevive a `/compact` y a sesiones nuevas, y se lee una sola vez al arrancar.

## Evidence

Esquema y patrón de acceso:

```markdown
## Hypotheses
- PII entra principalmente por el módulo de onboarding [src:grep auth/* @ 2026-05-30]

## Decisions
- Auditar por capa: ingress -> services -> storage [decided @ 2026-05-30]

## Findings
- services/user.py expone email sin redacción [src:user.py:88 @ 2026-05-30]
- storage/cache.go persiste DNI en claro [src:cache.go:42 @ 2026-05-30]

## Open
- Falta revisar exports/ y jobs/ batch
```

```python
# GOOD: read once, reference after; append only validated findings.
def bootstrap(ctx):
    if ctx.scratchpad_loaded:
        return ctx.memory            # reference, no re-read
    ctx.memory = parse_sections(read_file(".agent/scratchpad.md"))
    ctx.scratchpad_loaded = True
    return ctx.memory

def record_finding(f):
    assert f.validated and f.source
    upsert_section(".agent/scratchpad.md", "Findings",
                   f"- {f.text} [src:{f.source} @ {f.date}]")
```

Anti-patrón que se evita:

```python
# ANTI: state in conversation, file re-read and fully rewritten each turn.
def step(ctx):
    notes = read_file(".agent/notes.txt")      # re-read -> breaks cache
    ctx.history.append(notes + raw_tool_dump)  # unvalidated, in chat
    write_file(".agent/notes.txt", notes + raw_tool_dump)  # full rewrite
    # After /compact: nothing survives, modules get re-audited.
```

## Result

Archivo `.agent/scratchpad.md` con las cuatro secciones tipadas, bootstrap de lectura única en `ctx`, y `record_finding` que solo añade hallazgos validados con source y fecha. Los turnos siguientes referencian `ctx.memory` sin releer el archivo.

## Validation

- Solo conclusiones validadas: sí (assert validated + source).
- Esquema fijo Hipótesis/Decisiones/Hallazgos/Pendientes: sí.
- Lectura única + referencia: sí (flag `scratchpad_loaded`).
- Sobrevive a `/compact` y reset: sí — el estado se reconstruye solo desde el archivo.
- Evidencia por hallazgo (source + fecha): sí.

## Risks and Limits

- Si otro código hace `read_file` del scratchpad por turno, vuelve a romper el cache: auditarlo.
- El esquema debe permanecer fijo; añadir secciones ad hoc degrada la reconstrucción.
- `upsert_section` debe ser idempotente para no duplicar hallazgos al reintentar.
