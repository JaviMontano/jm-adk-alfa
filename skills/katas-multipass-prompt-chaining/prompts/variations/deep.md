<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multipass-prompt-chaining
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multipass Prompt Chaining Deep Variation

Usar cuando los schemas de transición no están definidos, el volumen de unidades es alto o la integración tiene impacto cross-file.

Incluir:

- **Discovery:** enumeración de unidades, dependencias entre ellas, volumen estimado y presupuesto de contexto por pase (Kata 11).
- **Diseño de schemas:** schema del pase 1 (`FileFindings` con estado de error tipado por unidad) y schema del pase 2 (`AuditReport`).
- **Estrategia de paralelismo:** mapeo del pase 1 a subagentes (Kata 4) y forma de recolección de salidas estructuradas.
- **Opciones consideradas:** chaining vs single-pass; justificación del overhead de coordinación.
- **Selected approach, validation y risks:** verificación de aislamiento, filtrado del pase 2 y conteo de unidades válidas frente a fallas silenciosas.
