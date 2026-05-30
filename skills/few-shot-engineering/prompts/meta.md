<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering Meta Prompt

Decide si la capacidad de few-shot engineering debe activarse y si es la herramienta correcta frente a alternativas.

## Activation Check

- El criterio es subjetivo y difícil de verbalizar, pero fácil de ejemplificar.
- El modelo falla en bordes pese a acertar en el caso típico.
- Existe un schema de salida estable.

## Descartar few-shot cuando

- El criterio es expresable como regla cerrada -> escribir la regla.
- El problema es de conocimiento factual -> usar contexto/RAG, no ejemplos.
- No hay casos de borde reales que justifiquen los ejemplos.

## Agentes a convocar

- Lead: construye el bloque.
- Support: detecta bordes no cubiertos y redundancias.
- Guardian: valida checklist y veta el anti-patrón.
- Specialist: aporta detalle de prefix caching cuando el coste importa.
