# Meta Prompt

Activa `katas-pretooluse-guardrails` sólo cuando haya una política que deba bloquear una tool antes de ejecutar.

## Activation Check

- ¿Hay side-effects que deben prevenirse antes de la llamada?
- ¿La política vive hoy en prompt o en lógica no determinística?
- ¿Se requiere `permissionDecision` `deny` o `ask`?
- ¿Existe una tool concreta y un `tool_input` verificable?

## Do Not Activate

- No hay tools ni side-effects.
- La tarea pide normalizar output después de ejecutar.
- La tarea sólo pide redacción de prompt.
- El input está vacío y no define regla ni tool.
