<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-mcp-server-configuration
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Example Output

## Summary

El server `crm` es config de equipo: va en `.mcp.json` versionado (project scope) para que toda la flota lo descubra. El `CRM_TOKEN` propuesto es un literal hardcodeado (anti-patron): debe inyectarse por env-var expansion.

## Result (GOOD)

```json
{
  "mcpServers": {
    "crm": {
      "command": "npx",
      "args": ["-y", "@acme/mcp-server-crm"],
      "env": { "CRM_TOKEN": "${CRM_TOKEN}" }
    }
  }
}
```

Cada dev exporta `CRM_TOKEN` en su entorno; el archivo versionado nunca contiene el secreto.

## Anti-patron (lo que se rechazo)

```json
{ "env": { "CRM_TOKEN": "crm_live_7Hk29ZqPmN4xR" } }
```

Token literal en archivo versionado. Si ya se commiteo: rotar el `CRM_TOKEN` en el CRM, reemplazar por `${CRM_TOKEN}` y purgar el historial con git filter-repo. Agregar `.mcp.json` a `.gitignore` NO remueve el secreto ya versionado.

## Validation

- Scope correcto: `.mcp.json` versionado (config de equipo, no `~/.claude.json`).
- Credencial via `${CRM_TOKEN}`, cero literales.
- Plan de remediacion ante leak explicitado (rotar + `${ENV}` + filter-repo).

## Risks and Limits

- Cada dev debe tener `CRM_TOKEN` exportado en su entorno o el server no conecta.
