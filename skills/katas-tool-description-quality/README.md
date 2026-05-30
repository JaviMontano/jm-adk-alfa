<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Tool Description Quality

Kata 21 del kit JM-ADK. La descripción de un tool es el único mecanismo que el modelo usa para escoger entre tools similares: input format, ejemplos de query y frontera explícita. Descripciones genéricas y solapadas (`Analyzes content` vs `Analyzes documents`) producen misroute en 20–30% de los turnos, invisible hasta que un downstream rompe. El remedio canónico: rename + split sobre overloading.

## Triggers

- tool description quality
- tool routing ambiguity
- rename split tools
- tool contract

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Quick Use

Actívala cuando dos o más tools confunden al modelo (respuestas correctas pero del tool equivocado), cuando diseñas una toolset nueva y quieres prevenir misroute, o cuando un tool acumula modos y conviene evaluar split. Entrega: tools renombrados con input format + frontera recíproca, y la justificación del rename/split.

## Output Format

Markdown con summary, evidence, result, validation, y risks.
