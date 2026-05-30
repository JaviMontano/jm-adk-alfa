<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-posttooluse-normalization
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Posttooluse Normalization Body of Knowledge

## Canon

Kata 03 del kit JM-ADK. Escenarios: Customer Support, Legacy ERP Integration.

### Conceptos clave

- **PostToolUse como garantía de runtime.** El hook matchea por patrón y aplica a TODAS las tools que matcheen. No es convención del autor de la tool: es el runtime el que asegura la transformación.
- **updatedMCPToolOutput.** Reemplaza el output crudo de la tool. El modelo nunca ve el XML legacy; solo el JSON canónico.
- **STATUS_MAP / esquemas de traducción.** Viven en código recargable, en un solo lugar. Códigos no contemplados caen en un fallback explícito (`"unknown"`).
- **additionalContext.** Anexa metadatos auditables (origen legacy, marca de normalización) sin contaminar el payload limpio que consume el modelo.

### Señales de calidad

| Señal | Objetivo |
|---|---|
| Garantía de runtime | El matcher cubre todas las tools legacy, no una por una |
| Output limpio | El XML crudo nunca entra al historial del modelo |
| Centralización | STATUS_MAP y esquemas en un único módulo recargable |
| Fallback explícito | Códigos sin mapear no se silencian; caen en "unknown" |
| Auditoría separada | additionalContext solo lleva metadatos, no el payload |

### Anti-patrón canónico

Cada tool decide si normaliza mediante decorators `@tool`. Funciona hasta que un handler nuevo olvida aplicar la regla y envenena el contexto con XML crudo. La fragilidad es estructural: la garantía depende de la disciplina de cada autor, no del runtime.

### Argumento de certificación

La normalización de outputs heterogéneos es responsabilidad del runtime vía PostToolUse, no convención de cada tool. Quiz de referencia: C·B·B (P1: el runtime SDK garantiza normalización para todas las tools que matcheen; P2: additionalContext para metadatos auditables que el modelo no necesita ver).

## Open Knowledge

- Conexión con extracción defensiva del tool_result (kata hermana): normalizar no exime de validar el shape antes de consumirlo.
- Hot-reload de STATUS_MAP sin reiniciar la sesión cuando aparecen códigos nuevos.
