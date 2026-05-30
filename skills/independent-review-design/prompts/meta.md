<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design Meta Prompt

Decide si `independent-review-design` debe activarse, si el alcance es seguro y qué agentes
de soporte participan.

## Activation Check

- Trigger match: el request menciona revisión, reviewer, per-file/cross-file o quorum.
- Domain fit: existe un pipeline que genera y luego revisa artefactos.
- Sufficient input: hay artefactos y un criterio de revisión, o un diseño de revisión a
  auditar.
- No safer specialized skill: si el foco es calibración de confidence y falsos positivos,
  prefiere `evaluation-confidence-design`.

## Routing

- Self-review detectado en la misma sesión, o quorum N-de-M presente: alta prioridad de
  activación (es el anti-patrón central).
- Pide al specialist el detalle de cómo aislar la sesión en el Agent SDK.
- Pide al guardian recorrer el checklist antes de cerrar.
