<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design Meta Prompt

Decide si `prompt-chaining-design` debe activarse, si el volumen justifica el chaining frente a un single-pass, y qué agentes de apoyo participan.

## Activation Check

- Coincide con los triggers (prompt chaining, multipass, transition schema, chained passes).
- Las unidades son procesables de forma independiente y solo se integran al final.
- El volumen excede lo que un single-pass procesa con calidad: si cabe holgado, NO activar (el chaining sería overhead injustificado).
- Hay input suficiente para definir la unidad atómica y el schema de transición.

## Agent Routing

- `lead` construye la cadena y los schemas.
- `support` audita acoplamiento entre unidades y fugas de crudos al pase 2.
- `guardian` valida el checklist y bloquea el anti-patrón del mega-prompt.
- `specialist` aporta el mapeo a Agent SDK / Claude Code (fan-out, salida estructurada).
