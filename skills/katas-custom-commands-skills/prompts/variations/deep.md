<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-custom-commands-skills
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 24 · Variación Deep · Slash Commands Custom y Skills

Usar cuando el caso es ambiguo, de alto impacto o cruza varios mecanismos de extensión.

Incluir:

- **Discovery:** inventario de lo que se quiere extender y de quién lo necesita (equipo vs personal).
- **Opciones consideradas:** command vs skill vs CLAUDE.md; project vs user scope; con o sin `context: fork`.
- **Enfoque elegido:** frontmatter completo (`name`, `description`, `context: fork`, `allowed-tools`, `argument-hint`) con justificación de cada campo.
- **Economía de contexto:** estimar el ruido evitado con `context: fork` (output verbose aislado en sub-agente, del orden de miles de tokens).
- **Validación:** confirmar que no se cayó en el anti-patrón y que las convenciones permanentes están en CLAUDE.md.
- **Riesgos:** scope incorrecto, whitelist demasiado amplia, regla permanente mal ubicada.
