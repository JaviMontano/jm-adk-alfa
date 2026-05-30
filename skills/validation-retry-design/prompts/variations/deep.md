<!--
generated-by: scripts/scaffold-skill.py
generated-for: validation-retry-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Validation Retry Design Deep Variation

Usar cuando la salida es de alto impacto, las reglas de validacion son ambiguas, o el reintento tiene efectos secundarios.

Incluye:

1. **Discovery:** que produce el paso, formato esperado, modos de falla observados, frecuencia.
2. **Diseno del validador:** reglas pass/fail, clasificacion recuperable vs no recuperable, forma del error accionable.
3. **Construccion del retry feedback:** como se reinyecta el error previo + salida previa + instruccion de correccion.
4. **Presupuesto y deteccion:** `max_retries`, contador, cadena de errores, deteccion de patron sistematico para fix estructural.
5. **Idempotencia:** como evitar duplicar efectos secundarios al reintentar.
6. **Escalada:** estado de salida con cadena completa de errores y handoff (humano o agente superior).
7. **Validacion:** checklist marcado + riesgos residuales.
