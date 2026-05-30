<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-tool-description-quality
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Tool Description Quality Meta Prompt

Decide si `katas-tool-description-quality` debe activarse para esta solicitud.

## Activation Check

- **Trigger match** — ¿menciona calidad de descripciones, routing ambiguo, rename/split de tools, o contrato de tool?
- **Domain fit** — ¿hay dos o más tools que el modelo confunde, o se diseña una toolset nueva con riesgo de misroute?
- **Sufficient input** — ¿se dispone de la definición de los tools (name + description) o al menos del síntoma?
- **No safer specialized skill** — para configuración de MCP servers usar `katas-mcp-server-configuration`; para escoger entre tools built-in de Claude Code usar `katas-builtin-tool-selection`.

## No activar cuando

- La solicitud no involucra selección entre tools (input vacío o tema ajeno).
- Se pide ignorar validación o evidencia.
