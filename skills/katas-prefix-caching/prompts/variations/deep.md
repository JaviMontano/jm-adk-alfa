<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Deep Variation

Usar cuando el prompt es grande, hay varios breakpoints de cache, o la fuga de costo no es obvia y hay que auditar `usage`.

Incluye: inventario de bloques clasificados (estático/dinámico) con justificación, dónde colocar cada `cache_control` ephemeral, qué valores volátiles se movieron del prefijo al `<reminder>`, la estimación de ahorro a partir de `cache_creation_input_tokens` vs `cache_read_input_tokens`, validación de que ningún cambio de un carácter invalida la zona estable, y riesgos.
