<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design Quick Variation

Úsala cuando el pipeline es simple y solo necesitas confirmar las tres garantías.

Verifica y reporta en tres líneas:

1. El reviewer corre en sesión limpia (sin contexto de generación). Sí/No.
2. per-file y cross-file están separados. Sí/No.
3. No hay quorum N-de-M que suprima hallazgos. Sí/No.

Devuelve el veredicto, el fix mínimo por cada "No" y los riesgos residuales.
