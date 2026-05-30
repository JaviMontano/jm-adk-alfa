<!--
generated-by: scripts/scaffold-skill.py
generated-for: session-lifecycle-management
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Example Input

Un agente de codificación pausó tras leer `auth/session.py`, `auth/token.py` y correr `pytest auth/`. Entre el turno anterior y ahora, un compañero hizo merge de un refactor que renombró `auth/` a `identity/` y cambió el `poetry.lock`. El objetivo del próximo turno es continuar arreglando el bug de expiración de token.

Decide la transición de ciclo de vida (resume / fork / fresh) y, si aplica, produce el `TypedSummary`.

Contexto disponible:

- `SessionContext.tool_results`: lectura de `auth/session.py` (mtime T0), lectura de `auth/token.py` (mtime T0), salida de `pytest auth/` (HEAD `abc123`).
- Estado actual del mundo: HEAD `def456`, `auth/` ya no existe, `poetry.lock` cambió de hash.
- Objetivo: continuar el fix de expiración de token.
