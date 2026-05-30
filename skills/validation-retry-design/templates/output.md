<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Output

## Resumen

{summary}

## Diseno del loop

- Paso validado: {paso}
- Formato esperado / schema: {schema}
- Presupuesto de reintentos: {max_retries}

## Validador (modo de falla)

{validador}  <!-- devuelve {ok, error, recoverable}; recuperable vs no recuperable -->

## Retry con error feedback

{retry_feedback}  <!-- como se reinyecta el error especifico previo, no el prompt original -->

## Politica de escalada

{escalada}  <!-- al agotar tope o ante falla no recuperable: cadena de errores + ultimo output -->

## Validacion (checklist)

- [ ] Feedback = error especifico previo, no prompt original
- [ ] Validador con causa accionable
- [ ] Recuperable reintenta / no recuperable escala
- [ ] Tope 2-3 con contador y cadena de errores
- [ ] Patron sistematico -> fix estructural
- [ ] Escalada explicita, sin salida fallida silenciosa

## Riesgos y limites

{risks}
