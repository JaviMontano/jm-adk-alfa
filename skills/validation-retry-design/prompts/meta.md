<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Meta Prompt

Decide si `validation-retry-design` debe activarse, si el alcance es seguro y que agentes de apoyo participan.

## Activation Check

- Trigger match: el pedido menciona retry, error feedback, validacion, recuperable vs no, o presupuesto de reintentos.
- Domain fit: existe un paso que produce salida estructurada que a veces falla validacion.
- Suficiente input: hay reglas de validacion y un formato esperado.
- No hay skill mas segura/especializada que aplique mejor.

## Senales de alcance seguro

- Hay un validador (o se puede construir) que devuelve causa accionable.
- Esta claro que es dato ausente (no recuperable) frente a error de formato (recuperable).
- El reintento no duplica efectos secundarios (idempotencia).

## Routing de agentes

- lead: construye el loop completo.
- support: caza reintento ciego, bucle infinito y falla silenciosa.
- guardian: valida checklist y veta el anti-patron.
- specialist: detalle de tool use / stop reasons / escalada en el SDK.
