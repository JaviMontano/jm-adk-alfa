<!--
generated-by: scripts/scaffold-skill.py
generated-for: adaptive-investigation-method
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Adaptive Investigation Method Primary Prompt

## Objective

Investigar un dominio desconocido (codebase, dataset o corpus) hasta resolver el objetivo del usuario, sin exceder el budget de exploracion y sin re-planificar de forma refleja.

## Required Inputs

- Objetivo concreto de la investigacion.
- Raiz del dominio (ruta del repo, dataset o coleccion de documentos).
- Budget duro: numero maximo de lecturas caras o tokens.
- Definition of done: que respuesta o artefacto cierra la investigacion.

## Process

1. **Fija el budget.** Declara `budget = N` y un scratchpad con `plan`, `hypotheses`, `findings`.
2. **Mapea barato.** Usa `Glob`/`Grep` para enumerar la superficie. No leas archivos completos en esta fase.
3. **Prioriza.** Escribe hipotesis ordenadas por valor esperado / costo, cada una ligada a nodos del mapa.
4. **Deep-dive selectivo.** Lee el nodo top-ranked con `Read`; decrementa el budget; registra el finding.
5. **Re-plan disciplinado.** Re-prioriza solo si la evidencia invalida la hipotesis activa. Si la confirma o la deja intacta, continua.
6. **Cierra.** Al agotar el budget o resolver el objetivo, sintetiza el deliverable desde `findings`.

## Output

Markdown segun `templates/output.md`: objetivo, budget consumido / total, mapa de superficie, hipotesis priorizadas, findings con referencia a nodo, decisiones de re-plan y deliverable final con riesgos residuales.
