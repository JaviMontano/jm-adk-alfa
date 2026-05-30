<!--
generated-by: scripts/scaffold-skill.py
generated-for: tool-use-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Tool Use Design

Capacidad de ingeniería para diseñar la descripción de cada tool como **contrato de routing** (propósito, input format, ejemplos y frontera recíproca) y aplicar la estrategia canónica de built-in tools `Grep → Read → Edit`, evitando descripciones genéricas y lecturas masivas que saturan la ventana de contexto.

## Resumen ejecutivo

La descripción de un tool es la única señal que el planner del modelo lee para elegir entre tools que compiten. Esta skill enseña a escribir esa descripción como contrato (no como documentación humana), a resolver el overloading con rename + split en lugar de prosa, a documentar el failure mode de Edit (anchor no único) con su fallback Read+Write, y a operar repos con `Grep → Read → Edit` sin `Glob("**/*") + Read all`.

## Triggers

- tool use design
- tool description contract
- builtin tool strategy
- tool routing

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Invócala cuando definas o refactorices el tool surface de un agente, cuando dos tools se solapen, cuando el modelo elija el tool equivocado, o cuando necesites un protocolo de lectura de repos que evite el read-all masivo. Entregable: un set de descripciones-contrato + el flujo `Grep → Read → Edit` validado contra el checklist.

## Output Format

Markdown con summary, evidence, result (bloque GOOD), anti-pattern (bloque ANTI), validation checklist y risks.
