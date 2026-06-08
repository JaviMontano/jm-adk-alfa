# Body Of Knowledge

## Canon

- `PreToolUse` corre antes de la invocación de una tool.
- `permissionDecision` es un enum estructurado: `allow`, `deny`, `ask`.
- `permissionDecisionReason` debe explicar la denegación para que el modelo pueda replanear.
- Las políticas críticas viven en `dict` o JSON recargable, no sólo en `system_prompt`.
- Un `deny` válido deja la tool sin ejecutar y por tanto sin side-effects.
- Un `raise` dentro de la tool no reemplaza el hook porque ocurre después de entrar a la tool.

## Quality Signals

| Signal | Target |
|---|---|
| Policy source | `dict` o JSON recargable |
| Hook event | `PreToolUse` |
| Decision output | `hookSpecificOutput` con `permissionDecision` |
| Deny case | cero side-effects |
| Allow case | conserva ruta válida |
| Injection case | prompt injection no cambia la decisión |

## Anti-Patterns

- Política escrita sólo en `system_prompt`.
- Validar después de ejecutar la tool.
- Retornar texto libre en lugar de `permissionDecision`.
- Omitir caso `allow`, causando falsos positivos.
- Usar matcher parcial sin justificar cobertura.

## Boundaries

- Para normalizar outputs después de la tool, usar `katas-posttooluse-normalization`.
- Para control del bucle agéntico, usar la kata de loop determinístico.
- Para errores estructurados de MCP, usar `katas-mcp-structured-errors`.
