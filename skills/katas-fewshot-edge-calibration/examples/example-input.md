<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-fewshot-edge-calibration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Input

Escenario: equipo de soporte necesita clasificar tickets entrantes en `clase` (billing, feedback, auth, ...) y `urgencia` (high, low). El prompt actual usa prosa abstracta y la clasificación sale inconsistente turno a turno.

Petición: "Necesito que el clasificador de tickets sea consistente. Hoy le digo 'clasifica usando criterio profesional, considerando urgencia, dominio, impacto, severidad operacional, prioridad SLA y política interna' y los resultados varían. Calíbralo con few-shot."

Casos de borde del dominio disponibles:

- "no me llega la factura desde hace 3 meses" → billing / high
- "tengo una sugerencia para la app" → feedback / low
- "no puedo entrar, token expirado" → auth / high
