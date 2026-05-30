<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-session-resume-fork
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Kata 25 · Plantilla de salida

## Decisión

{resume | fork | fresh}

## Justificación

{por qué el contexto previo es válido / por qué se necesitan ramas paralelas / por qué los tool results están stale}

## Comando

```bash
{comando ejecutable: claude --resume ... | claude --fork ... --new-name ... | SUMMARY=$(cat scratchpad.md); claude -p "..."}
```

## Summary inyectado (si fresh)

{campos tipados desde el scratchpad estructurado; fuentes recargadas}

## Validación

{confirmación de que no se pega transcript crudo y de que el contexto reanudado refleja el estado actual}

## Riesgos y límites

{ramas que podrían mezclarse, fuentes que podrían seguir stale}
