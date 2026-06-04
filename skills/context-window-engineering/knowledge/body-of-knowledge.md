# Context Window Engineering Body of Knowledge

## Canon

La ventana de contexto se ensambla, no se acumula. Dos fuerzas la gobiernan:

1. **Prefix caching (KV cache).** El modelo cachea el estado KV del prefijo y lo reutiliza mientras los tokens sean idénticos byte a byte. Un prefijo estable rinde reuso cercano a ~10x en latencia/costo. El cache se invalida en el primer byte que difiere: por eso el orden es **estático-first / dinámico-last**.
2. **Dilución softmax (curva en U / lost-in-the-middle).** La atención no es uniforme: es alta en los bordes (inicio y fin) y baja en el centro. Una regla crítica enterrada en el medio de un contexto largo se diluye y el modelo "la olvida".

### Conceptos clave

- **Estático-first:** rol, herramientas, políticas y esquema al inicio, byte-idénticos entre turnos.
- **Dinámico-last:** estado volátil (timestamp, contadores, último turno) en un bloque `<reminder>` al final.
- **Edge placement:** las reglas que no pueden olvidarse van en los bordes (inicio + reafirmadas al final).
- **Compactación por umbral:** al superar un porcentaje de ocupación (>55%), se resume el historial intermedio preservando los bordes y la estabilidad del prefijo.

### Decisión de diseño

Cualquier dato que cambie por-turno NO puede vivir en el prefijo: su sola presencia invalida el cache completo. Si un dato es crítico Y dinámico, va en el `<reminder>` final (borde) — nunca en el prefijo ni en el centro.

## Quality Signals

| Signal | Target |
|---|---|
| Estabilidad del prefijo | Byte-idéntico entre turnos; sin valores por-turno |
| Cache-hit rate | Alto y estable turno a turno (cache-read >> cache-write) |
| Retención de regla crítica | La regla sobrevive a una prueba de contexto largo |
| Edge placement | Reglas críticas en inicio + reafirmadas al final |
| Política de compactación | Umbral explícito (>55%) que preserva los bordes |
| Update safety | Overrides locales y archivos manuales preservados |

## Anti-patrón

Poner un timestamp (o cualquier valor por-turno) al inicio del contexto invalida el prefix cache en cada turno; enterrar la regla crítica en el centro la expone a la dilución softmax. Ambos errores suelen coexistir y, sin umbral de compactación, empeoran a medida que crece el historial.

## Open Knowledge

- Mapear cada patrón al mecanismo concreto de caching del proveedor (cache breakpoints / `cache_control`).
- Añadir métricas observadas de cache-hit por proyecto a medida que se estabilicen.
