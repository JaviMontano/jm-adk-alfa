<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Quick Variation

Usar cuando el prompt es pequeño y la clasificación estático/dinámico es obvia.

Aplica la regla directamente: estático arriba con `cache_control: {type: "ephemeral"}`, dinámico al final en `<reminder>`. Devuelve solo el prompt reordenado y, si hay `usage`, la comparación `cache_read_input_tokens` vs `cache_creation_input_tokens`.
