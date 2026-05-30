<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation

Mitigacion de dilucion softmax: edge placement de reglas criticas y compactacion al cruzar 50-60 por ciento de contexto.

## Triggers

- context dilution
- lost in the middle
- edge placement
- context compaction

## Allowed Tools

- Read
- Grep
- Glob
- Bash

## Resumen ejecutivo

La atención del transformer sigue una curva en U: los bordes del prompt reciben atención alta y el centro se diluye ("lost in the middle"). Esta skill aplica dos disciplinas: colocar reglas críticas en los bordes (edge placement, repitiéndolas al final como `<reminder>`) y compactar el historial cuando `usage_fraction > 0.55`, preservando reglas, decisiones y escaladas. Evita la violación silenciosa de políticas en conversaciones largas.

## Quick Use

Actívala al diseñar system prompts o agentes multi-turno con políticas de seguridad/compliance que deben sostenerse a lo largo de muchos turnos, o cuando un agente respeta una regla temprano y la viola después. Coloca las reglas críticas al inicio Y al final del prompt; pon los datos ricos al centro; compacta antes del 60% de contexto.

## Output Format

Markdown con summary, evidence, result, validation y risks.
