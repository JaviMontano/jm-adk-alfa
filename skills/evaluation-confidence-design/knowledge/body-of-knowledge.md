# Evaluation Confidence Design Body of Knowledge

## Canon

La capacidad consiste en hacer que la evaluación de un agente sea fiable en producción separando tres cosas que suelen confundirse: el **score crudo** que emite el modelo, la **probabilidad calibrada** de que un hallazgo sea correcto, y la **decisión** de aceptarlo. El corte de aceptación se hace siempre sobre la probabilidad calibrada contra un labeled set, nunca sobre el score crudo.

## Conceptos clave

- **Confidence calibrada vs cruda.** El `confidence` que reporta un modelo no es una probabilidad: 0.8 no significa "acierta 80% de las veces". La calibración mapea el score crudo a la precisión observada en el labeled set (binning, isotonic, Platt).
- **Labeled set / ground truth.** Conjunto de ejemplos etiquetados por humano como positivo/negativo, anotados además por `document_type` y por categoría. Es la única fuente de verdad para calibrar.
- **Stratified sampling.** Muestrear por estrato (`document_type` u otra dimensión de riesgo) con mínimo garantizado por estrato, en vez de aleatorio global, para que los estratos raros no desaparezcan de la métrica.
- **Criterio categórico.** Definición de cada categoría con ejemplos positivos y negativos por nivel de severidad, en lugar de instrucciones vagas tipo "be conservative".
- **FP rate por categoría.** Tasa de falsos positivos calculada por categoría, no agregada. Una categoría ruidosa puede arruinar la precisión sin que la métrica global lo muestre.
- **Disable temporal.** Flag para desactivar una categoría con FP alto mientras se rediseña su criterio, sin tumbar el resto del evaluador.

## Quality Signals

| Signal | Target |
|---|---|
| Calibración | El umbral usa confidence calibrada contra el labeled set, no la cruda |
| Estratificación | Muestreo por `document_type` con mínimo por estrato |
| Criterios categóricos | Cada categoría con ejemplos +/- por severidad |
| FP desglosado | Se reporta FP rate por categoría, no solo accuracy agregada |
| Aislamiento | Disable temporal disponible para categorías de alto FP |

## Decisión de diseño

¿Confidence cruda o calibrada para el corte? Siempre calibrada. ¿Muestra global o estratificada? Estratificada cuando el riesgo varía por `document_type`. ¿Accuracy agregada o FP por categoría? Por categoría como métrica primaria; la agregada es secundaria.

## Anti-patrón

Confiar en la `confidence` cruda como umbral, muestrear globalmente, redactar criterios vagos ("be conservative") y reportar una accuracy agregada que esconde el sesgo por categoría. Ver `scripts/qa/run-confidence-fp-tests.py`.
