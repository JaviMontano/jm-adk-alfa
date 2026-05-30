<!--
generated-by: scripts/scaffold-skill.py
generated-for: few-shot-engineering
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Few Shot Engineering Body of Knowledge

## Canon

Few-shot engineering es la capacidad de **calibrar bordes subjetivos** mostrando ejemplos en vez de describir criterios. El núcleo del canon:

- **Bordes, no centro.** Un ejemplo del caso típico no aporta información; el modelo ya lo resuelve. El valor está en los casos límite, las zonas grises y las decisiones donde el schema deja ambigüedad.
- **Mismo schema de salida.** Cada ejemplo debe usar el formato exacto de producción. El few-shot enseña forma y juicio simultáneamente; un ejemplo con otro formato envenena la salida.
- **2–4 ejemplos.** Por debajo de 2 no hay calibración; por encima de 5 la atención se dispersa y el coste de tokens sube sin ganancia.
- **Al inicio, zona estática.** Los ejemplos van antes de la entrada variable del usuario para que el prefijo del prompt sea estable y el prefix cache se reutilice entre llamadas.
- **Complementar, no contradecir.** Ningún ejemplo debe romper el schema ni contradecir a otro ejemplo; dos ejemplos con reglas opuestas dejan al modelo peor que sin few-shot.

## Conceptos clave

| Concepto | Definición |
|---|---|
| Borde / zona gris | Caso donde el criterio es ambiguo y el modelo tiende a fallar |
| Schema de salida | Estructura exacta esperada en producción (claves, tipos) |
| Zona estática | Parte del prompt que no cambia entre llamadas; cacheable |
| Prefix cache | Reutilización del prefijo de prompt ya procesado; se invalida si el prefijo cambia |
| Complementariedad | Propiedad de que los ejemplos no se contradicen entre sí ni con el schema |

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Cobertura de bordes | Cada ejemplo ilustra una decisión de borde distinta |
| Fidelidad de schema | Los ejemplos usan el formato exacto de producción |
| Economía de ejemplos | Entre 2 y 4, ninguno redundante |
| Estabilidad de cache | El bloque está al inicio; nada variable lo precede |
| No contradicción | Ningún par de ejemplos sugiere reglas opuestas |

## Decisión de diseño

¿Few-shot o regla? Si el criterio es expresable de forma cerrada, escribe la regla (es más barato y auditable). Usa few-shot solo cuando el criterio es difícil de verbalizar pero fácil de **ejemplificar**. Si el problema es de conocimiento factual, no uses ejemplos: usa contexto/RAG.

## Anti-patrón

Criterio en prosa abstracta ("usa tu buen juicio"), más de 5 ejemplos, ejemplos del caso típico en vez de bordes, o ejemplos rotados/colocados después de la entrada variable (rompen el prefix cache y dispersan la atención).

## Open Knowledge

- Documentar qué bordes específicos del proyecto resultaron más sensibles a la calibración a medida que se estabilizan.
