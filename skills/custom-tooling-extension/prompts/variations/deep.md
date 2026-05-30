<!--
generated-by: scripts/scaffold-skill.py
generated-for: custom-tooling-extension
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Custom Tooling Extension Deep Variation

Úsala cuando la decisión es ambigua o de alto impacto: command vs skill no obvio, la extensión muta el repo/sistema, debe replicarse a todo el equipo, o compone varios artefactos (command que delega en skill, skill que orquesta sub-agentes).

Incluye:

- **Discovery**: triggers, scope requerido (project vs user), superficie de herramientas, convenciones del proyecto ya existentes.
- **Opciones**: command vs skill; con/sin `context: fork`; whitelist de `allowed-tools` por opción.
- **Decisión**: artefacto y scope elegidos con justificación, y qué reglas migran a `CLAUDE.md`.
- **Validación**: corrida del checklist completo y de los evals (incluidos los negativos).
- **Riesgos**: blast radius, replicabilidad y contaminación de contexto residuales.
