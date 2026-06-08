# Meta Prompt

Activa `katas-provenance-preservation` cuando un reporte factual deba ser auditable claim por claim.

## Activation Check

- ¿Hay múltiples fuentes o subagentes?
- ¿Hay claims factuales que requieren source_id?
- ¿Existe riesgo de contradicción entre fuentes?
- ¿El usuario pide preservar "quién dijo qué"?

## Do Not Activate

- No hay claims factuales ni fuentes.
- La tarea es redacción general.
- El input está vacío.
- El usuario exige ignorar provenance y no hay forma segura de cumplir.
