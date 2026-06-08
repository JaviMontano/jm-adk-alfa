# Body Of Knowledge

## Canon

- `PostToolUse` transforma output después de ejecutar una tool y antes del historial del modelo.
- `updatedMCPToolOutput` reemplaza el output crudo que verá el modelo.
- `additionalContext` agrega metadatos auditables y no debe contener payload crudo.
- `STATUS_MAP` y schemas de traducción deben vivir en un punto recargable.
- Códigos no mapeados deben caer en fallback explícito `unknown`.

## Quality Signals

| Signal | Target |
|---|---|
| Hook event | `PostToolUse` |
| Output reemplazado | `updatedMCPToolOutput` con JSON parseable |
| Raw oculto | XML no entra al historial |
| Matcher | cubre todas las tools legacy |
| Fallback | `unknown` para códigos no mapeados |

## Anti-Patterns

- Normalización por-tool como garantía principal.
- XML crudo dentro de `updatedMCPToolOutput`.
- Payload crudo dentro de `additionalContext`.
- Sin fallback para estados desconocidos.
- Matcher que sólo cubre un handler conocido.
