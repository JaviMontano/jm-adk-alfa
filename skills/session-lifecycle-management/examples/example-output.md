<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Output

## Decisión de transición

**fresh** + `TypedSummary`.

**Razón:** el HEAD cambió (`abc123` → `def456`), `auth/` fue renombrado a `identity/` y el `poetry.lock` cambió de hash. Las tres tool results del scratchpad apuntan a rutas que ya no existen: son stale críticas. Un `resume` reusaría rutas muertas y haría que el agente edite archivos inexistentes.

## Evidencia de staleness

| Tool result | Fuente | Señal | Estado |
|---|---|---|---|
| read auth/session.py | auth/session.py | path inexistente (renombrado a identity/) | stale |
| read auth/token.py | auth/token.py | path inexistente (renombrado a identity/) | stale |
| pytest auth/ | HEAD del árbol | abc123 → def456 | stale |

## TypedSummary

```json
{
  "goal": "Arreglar el bug de expiracion de token",
  "decisions": ["El fix vive en la logica de TTL del token"],
  "open_questions": ["Donde quedo la logica de token tras el rename a identity/?"],
  "verified_facts": [],
  "stale_dropped": ["auth/session.py", "auth/token.py", "pytest auth/ @ abc123"]
}
```

## Anti-ejemplo (lo que NO se debe hacer)

```python
# ANTI: resume ciego — el agente intentaria editar auth/token.py, que ya no existe,
# y trataria la salida vieja de pytest como verde aunque el arbol cambio.
Session(context=prev_transcript, goal="fix token expiry")
```

## Validación

- [x] Staleness detectada contra la fuente (paths + HEAD)
- [x] Summary tipado (no transcript crudo)
- [x] Forks no aplican (objetivo único)
- [x] Transición trazada con su razón
- [x] Stale crítico forzó `fresh`

## Riesgos y límites

- Hay que re-descubrir la nueva ruta (`identity/`) en el próximo turno antes de editar; queda como `open_question`.
