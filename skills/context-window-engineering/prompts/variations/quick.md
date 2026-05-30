<!--
generated-by: scripts/scaffold-skill.py
generated-for: context-window-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Context Window Engineering Quick Variation

Úsala cuando el contexto ya está casi bien ordenado y solo hay que verificar/ajustar.

Pasos: confirma que el prefijo es byte-idéntico (sin timestamp ni valores por-turno), que el estado volátil está en el `<reminder>` final y que las reglas críticas están en los bordes; revisa que exista umbral de compactación.

Devuelve solo: el ajuste aplicado (o "ya correcto"), el resultado del checklist y los riesgos residuales.
