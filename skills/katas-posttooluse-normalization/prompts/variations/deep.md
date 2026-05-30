<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization Deep Variation

Úsala cuando hay muchas tools heterogéneas, formatos legacy ambiguos, payloads anidados o impacto cross-tool.

Incluye: inventario de todas las tools y sus formatos crudos; diseño del matcher único de `PostToolUse`; construcción y gobierno de `STATUS_MAP` (códigos sin mapear, fallback a `"unknown"`); opciones consideradas (hook central vs. por-tool) y por qué el central gana el argumento de runtime; el handler completo; uso de `additionalContext` para auditoría; validación de que el XML crudo nunca entra al historial; riesgos (tools nuevas que escapen al matcher, hot-reload de esquemas).
