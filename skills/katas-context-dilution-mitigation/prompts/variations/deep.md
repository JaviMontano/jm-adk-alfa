<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-context-dilution-mitigation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Context Dilution Mitigation Deep Variation

Úsala cuando el agente es multi-turno, de alto impacto (compliance/seguridad) o cuando hay que diseñar la estrategia de compactación de cero.

Incluye:
- Mapa de la curva en U para el prompt concreto: qué reglas están en el valle y cómo migrarlas a los bordes.
- Diseño del `<reminder>` final y verificación de que duplica exactamente las reglas del inicio.
- Definición de `usage_fraction` contra la ventana real del modelo y justificación del umbral elegido (50-60%).
- Diseño de `compact(history, preserve=['rules','decisions','escalations'])`: qué se condensa y qué se conserva intacto.
- Conexión con `katas-persistent-scratchpad` para lo que debe sobrevivir fuera del historial.
- Tests estructurales, opciones consideradas, enfoque seleccionado, validación y riesgos.
