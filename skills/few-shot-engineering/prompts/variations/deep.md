<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering Deep Variation

Usar cuando los bordes son muchos, el coste de tokens importa o hay riesgo de contradicción entre ejemplos.

1. Inventaria todos los bordes candidatos a partir de fallos reales.
2. Agrúpalos por decisión y elige un único ejemplo representativo por grupo (máx 4).
3. Verifica complementariedad par a par: ningún ejemplo debe sugerir una regla opuesta a otro.
4. Marca la frontera del prefijo estático para que el prefix cache se reutilice.
5. Valida contra un set de bordes retenidos y mide la mejora en la decisión gris.

Incluye: notas de descubrimiento de bordes, opciones consideradas, set final de ejemplos con justificación, evidencia de validación y riesgos.
