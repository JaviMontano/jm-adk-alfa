<!--
generated-by: scripts/scaffold-skill.py
generated-for: evaluation-confidence-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Evaluation Confidence Design Deep Variation

Úsala cuando no hay labeled set fiable, el evaluador va a producción de alto impacto, o varias categorías arrastran falsos positivos.

1. **Discovery:** inventaría fuentes de etiquetas, distribución por `document_type`, balance positivo/negativo y cómo emite el agente su `confidence`.
2. **Opciones de calibración:** compara binning vs isotonic vs Platt; documenta por qué eliges una y cómo se refresca al cambiar de modelo.
3. **Estratificación:** define estratos y mínimo por estrato; justifica los estratos raros.
4. **Criterios categóricos:** redacta cada categoría con ejemplos +/- por severidad; identifica candidatas a disable temporal.
5. **Validación:** corre `scripts/qa/run-confidence-fp-tests.py`, reporta accuracy y FP por estrato y categoría, y registra los supuestos del calibration map.

Incluye notas de discovery, opciones consideradas, enfoque elegido, validación y riesgos residuales.
