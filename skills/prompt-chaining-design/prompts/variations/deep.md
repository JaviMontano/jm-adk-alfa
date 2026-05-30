<!--
generated-by: scripts/scaffold-skill.py
generated-for: prompt-chaining-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Prompt Chaining Design Deep Variation

Úsala cuando la granularidad de la unidad es ambigua, hay dependencias entre unidades, o el costo/latencia del chaining es crítico.

Incluye: análisis de candidatos de unidad atómica y por qué se elige uno; el schema completo del pase local con todos los campos que el pase de integración necesitará (para garantizar que nunca abra un crudo); el schema de transición versionado; la estrategia de paralelización del map y el reduce tolerante a errores; la comparación cuantitativa frente a single-pass (volumen, tokens, latencia, aislamiento); validación contra el checklist completo; y riesgos residuales (unidades acopladas, deriva de schema entre versiones).
