# Meta Prompt

Activa `katas-posttooluse-normalization` cuando el problema sea limpiar output después de ejecutar una tool y antes del historial del modelo.

## Activation Check

- ¿Hay XML, códigos opacos o payload legacy?
- ¿Se menciona `PostToolUse` o `updatedMCPToolOutput`?
- ¿La garantía debe ser central por runtime?
- ¿El usuario pide que el modelo no vea payload crudo?

## Do Not Activate

- La tarea bloquea una tool antes de ejecutar.
- La tarea sólo valida un JSON ya limpio.
- No hay tool output ni payload crudo.
- El input está vacío y no define formato origen ni destino.
