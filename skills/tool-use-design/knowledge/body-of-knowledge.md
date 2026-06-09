# Tool Use Design Body of Knowledge

## Canon

La descripción de un tool es un **contrato de routing**, no documentación humana. Es la única señal que el planner del modelo lee para decidir, sin contexto adicional, cuándo invocar un tool y con qué forma de entrada. Por eso una descripción canónica contiene cuatro piezas: propósito en una frase, **input format** explícito, 1–2 ejemplos de invocación y la **frontera recíproca** ("usa X para A; para B usa Y", y la vecina dice lo simétrico). La estrategia de operación sobre repos es `Grep → Read → Edit`: localizar barato, leer selectivo, mutar preciso.

## Conceptos clave

- **Descripción-contrato:** el modelo enruta por la descripción, no por el nombre. Sin input format ni frontera, la selección es una adivinanza.
- **Frontera recíproca:** cada descripción declara qué hace y qué NO hace, delegando explícitamente en su tool vecina. La reciprocidad elimina el solapamiento.
- **Overloading → rename + split:** un tool que hace dos cosas se divide en dos tools con fronteras claras; nunca se resuelve con un párrafo de matices en la descripción.
- **Estrategia Grep→Read→Edit:** Grep/Glob localizan, Read lee solo lo relevante, Edit muta. Es el flujo que minimiza tokens y maximiza precisión.
- **Edit failure mode:** el anchor (`old_string`) debe ser único; si no, Edit falla. **Fallback:** Read + Write para reescritura total.

## Señales de calidad

| Señal | Objetivo |
|---|---|
| Frontera recíproca | Cada par de tools que compite tiene delegación en ambos sentidos |
| Routing inmediato | El modelo elige el tool correcto sin pedir aclaración |
| Input format | Cada descripción declara la forma de entrada + 1–2 ejemplos |
| Edit safety | El failure mode (anchor no único) tiene fallback Read+Write documentado |
| Economía de contexto | Flujo `Grep → Read → Edit`, sin `Glob("**/*") + Read all` |
| Determinismo | Reporte validable offline contra `assets/tool-use-contract.json` |

## Decisión de diseño

¿Dos tools se solapan? → **split + rename** con fronteras recíprocas, no prosa.
¿Necesitas entender un repo? → **Grep para localizar**, luego **Read selectivo**, nunca read masivo.
¿Edit falla por anchor ambiguo? → aísla un anchor único o cae al **fallback Read+Write**.

## Anti-patrón

Descripciones genéricas (`"Analyzes content"`, `"Processes the file"`) sin input format ni frontera, que obligan al modelo a adivinar el tool; y `Glob("**/*") + Read all` upfront (~200k tokens) que satura la ventana antes de empezar.

## Evidencia Requerida

- Tool contracts con purpose, input_format, examples y boundary.
- Pares de frontera recíproca entre tools que compiten.
- Decisión `rename_split` para tools sobrecargadas.
- Estrategia `grep -> read -> edit` sin read-all.
- `Edit` failure mode y fallback.
- Validación offline con `scripts/validate_tool_use_design.py`.
