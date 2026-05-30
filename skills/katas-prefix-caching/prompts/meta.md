<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-prefix-caching
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Prefix Caching Meta Prompt

Evaluar si `katas-prefix-caching` debe activarse y qué agentes de soporte participan.

## Activation Check

- ¿El request toca organización del prompt para reuso de cache, `cache_control` ephemeral, prefijo estático vs sufijo dinámico, o lectura de tokens de cache en `usage`? (trigger match)
- ¿El problema es una fuga de costo por dato dinámico en el prefijo, o ineficiencia de cache KV? (domain fit)
- ¿Hay un prompt o un `usage` concreto sobre el que actuar? (sufficient input)
- Si el problema real es dilución de atención en el centro del prompt, derivar a `katas-context-dilution-mitigation`; si es memoria persistente entre sesiones, a `katas-persistent-scratchpad`.
