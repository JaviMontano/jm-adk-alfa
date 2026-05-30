<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-hierarchical-claude-memory
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Hierarchical Claude Memory · Output

## Summary

{Qué se diseñó o auditó en la memoria jerárquica y el resultado neto.}

## Niveles de memoria

```text
# ~/.claude/CLAUDE.md  (usuario)
{preferencias personales}

# <repo>/CLAUDE.md  (equipo)
{secciones con @imports + prohibiciones cortas}

# <repo>/<subpath>/CLAUDE.md  (módulo)
{reglas locales justificadas por especificidad}
```

## Evidence

- {Decisiones de nivel y precedencia, con justificación.}

## Validation

- Preferencias personales fuera del repo: {sí/no}
- Nivel equipo modularizado con `@imports`: {sí/no}
- Precedencia subpath > repo > user aplicada: {sí/no}
- Archivo principal corto / caché-friendly: {sí/no}

## Risks and Limits

- {Riesgos residuales, conflictos no resueltos, supuestos.}
