# Example Input

Tenemos un agente que revisa contratos y emite hallazgos de riesgo con un campo `confidence` (0-1) por hallazgo, en categorías `indemnity`, `termination`, `data_privacy`, `payment_terms`. Hoy aceptamos todo hallazgo con `confidence >= 0.7` y reportamos una accuracy global del 88%.

El equipo legal se queja de demasiados falsos positivos en `data_privacy` sobre `document_type = NDA`, pero la accuracy global sigue luciendo bien. Tenemos 600 hallazgos etiquetados por humano (positivo/negativo) con su `document_type` y categoría.

Diseña la evaluación correcta: corte calibrado, muestreo estratificado por `document_type`, criterios categóricos y FP rate por categoría, con capacidad de desactivar temporalmente `data_privacy` si su FP rate es inaceptable.
