<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering Deep Variation

Úsala cuando el agente "olvida" reglas en sesiones largas, el cache-hit es bajo, o hay que rediseñar el assembler completo con compactación.

Incluye:

- **Discovery:** inventario de bloques actuales, qué cambia por-turno, dónde están hoy las reglas críticas, métricas de cache observadas.
- **Diagnóstico:** ¿hay valores por-turno en el prefijo? ¿reglas en el centro (curva en U)? ¿falta umbral de compactación?
- **Opciones:** ordenamientos candidatos, dónde colocar el `<reminder>`, qué resumir vs preservar literal en la compactación.
- **Diseño elegido:** assembler estático-first / dinámico-last con edge placement y umbral, mapeado al mecanismo de caching del proveedor.
- **Validación:** plan de medición de cache-hit y prueba de retención de regla crítica en contexto largo.
- **Riesgos:** invalidaciones de cache por cambios de tokenizer/cliente, pérdida de bordes al compactar.
