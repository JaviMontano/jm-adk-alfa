<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-adaptive-investigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Adaptive Investigation Primary Prompt

## Objective

Investigar un dominio o repositorio desconocido aplicando el patron de la Kata 19: mapeo barato, presupuesto acotado y re-plan disciplinado.

## Required Inputs

- Objetivo de la investigacion (que se quiere entender o encontrar).
- Alcance: repositorio, carpeta o documento de partida.
- Presupuesto de exploracion: maximo de archivos / queries / minutos.
- Definicion de done (que cierra la investigacion).

## Process

1. **Mapeo barato.** Usa `Glob` sobre nombres y `Grep` sobre imports/simbolos para obtener la topologia. No leas cuerpos completos todavia.
2. **Priorizacion declarada.** Construye un plan ordenado a partir de la topologia y enuncia por que cada objetivo esta arriba.
3. **Deep-dive selectivo.** Con `Read`, profundiza SOLO en los objetivos priorizados, descontando del presupuesto en cada paso.
4. **Re-plan condicional.** Re-planifica SOLO si un hallazgo invalida la hipotesis vigente; si solo la refina, continua sin re-plan.
5. **Persistencia.** Anota plan y `Hallazgos` en el scratchpad. Al agotar presupuesto, reporta encontrado + pendiente.

## Output

Return the deliverable in this shape: Markdown with summary, evidence, result, validation, and risks. Incluye el presupuesto consumido y los re-planes disparados con su justificacion.
