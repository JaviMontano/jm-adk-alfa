<!--
generated-by: scripts/scaffold-skill.py
generated-for: katas-multiagent-error-propagation
generated-on: 2026-05-29
overwrite-policy: missing-only unless --force
-->

# Katas Multiagent Error Propagation Deep Variation

Úsala cuando hay que diseñar la orquestación completa o auditar por qué un report multi-agente produjo un hueco silencioso.

Incluye: mapa de coordinador + subagentes y sus fuentes; el contrato de propagación por subagente (`failure_type`, `attempted_query`, `partial_results`, `suggested_alternatives`); la estrategia de local recovery (qué transients se reintentan y con qué); la matriz access failure vs valid empty; cómo el synthesis consume `partial_results` y anota coverage gaps; y la política del coordinador ante `retryable=False`. Cierra con validación y riesgos residuales.
