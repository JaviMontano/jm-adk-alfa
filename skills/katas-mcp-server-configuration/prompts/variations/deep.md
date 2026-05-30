<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 22 · Deep Variation

Usa cuando el scope es ambiguo, hay un secreto filtrado, o el cambio afecta a toda la flota.

Incluye: decision de scope justificada (equipo vs personal), opciones de built-in vs MCP consideradas, plan de remediacion ante leak (rotar credencial + `${ENV}` + git filter-repo para purgar historial), validacion de que ningun token queda literal, y riesgos residuales (env-vars ausentes en el entorno de algun dev).
