# Provenance Engineering Body of Knowledge

## Canon

La provenance es la cadena de custodia de un dato: de qué fuente salió, dónde dentro de ella, y con qué fecha. La capacidad consiste en hacer esa cadena **estructural**, no documental. Conceptos centrales:

- **Claim tipado.** Cada afirmación es un objeto con `value`, `source[]` no vacío y `as_of`. La invariante "no hay claim sin source" se enforza por construcción (constructor/schema), de modo que un claim sin fuente no puede existir, no solo "no debería".
- **Provenance en origen.** La fuente se captura en el momento de la extracción (id, ubicación: página/span/celda, fecha del documento). Recuperarla después es imposible o falible.
- **Conflicto preservado.** Cuando dos fuentes afirman valores distintos del mismo atributo, se marca `conflict=true` y se conservan **todas** las fuentes. Promediar, votar o elegir la primera destruye información que el humano necesita.
- **Escalación, no resolución.** El pipeline no decide cuál fuente gana; enruta el conflicto a un humano con ambas fuentes y la fecha visible.
- **Test estructural.** Un test recorre el output y falla si aparece un claim sin source o un conflicto silenciado. Es el gate que convierte la invariante en garantía.

## Quality Signals

| Signal | Target |
|---|---|
| Cobertura de source | 100% de claims con `source[]` no vacío (id + ubicación + fecha) |
| Marcado de conflicto | Todo desacuerdo entre fuentes lleva `conflict=true` con todas las fuentes |
| Política de conflicto | Conflictos escalados a humano, nunca promediados ni colapsados |
| Visibilidad de fecha | `as_of` visible para el humano en el render |
| Gate estructural | Test que falla ante claim sin source o conflicto enmascarado |

## Decisión de diseño

Modela `Claim` como tipo con invariante en el constructor en lugar de validar provenance "al final". Validar al final permite que claims sin source existan en memoria y se fuguen por rutas no testeadas; el constructor los hace imposibles. Para conflictos, prefiere conservar y escalar antes que cualquier heurística de resolución automática: la heurística que parece razonable hoy (la fuente más reciente gana) produce datos que ninguna fuente afirma y rompe la auditabilidad.

## Anti-patrón

Resumen en prosa sin `source_id`, sin fecha y sin señal de conflicto. Variante peligrosa: promediar dos cifras contradictorias en un único número. El humano queda sin forma de auditar el origen ni de saber que hubo desacuerdo.

## Open Knowledge

- Normalización de valores para distinguir conflicto real de diferencia de formato.
- Propagación de `source[]` en claims derivados (sumas, dedupe, joins).
- Uso de `assets/structural-test-policy.json` como contrato minimo cuando el lenguaje o framework cambia.
