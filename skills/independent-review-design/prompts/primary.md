<!--
generated-by: scripts/scaffold-skill.py
generated-for: independent-review-design
generated-on: 2026-05-30
overwrite-policy: missing-only unless --force
-->

# Independent Review Design Primary Prompt

## Objective

Diseñar (o auditar) la etapa de revisión de un pipeline de generación para que cumpla:
reviewer independiente en sesión limpia, pases per-file y cross-file separados, y reporte
sin quorum que suprima señal rara.

## Required Inputs

- Goal: qué pipeline/artefactos se revisan y con qué criterio.
- Context: cómo se genera hoy, cómo se revisa hoy, qué contexto comparte el reviewer.
- Constraints: lenguaje, runtime, presupuesto de pasadas, severidad.
- Definition of done: el checklist de validación pasa.

## Process

1. Identifica qué contexto del generador llega al reviewer y córtalo (sesión limpia).
2. Especifica el pase per-file: por archivo, defectos locales con cita archivo:línea.
3. Especifica el pase cross-file por separado: inconsistencias y contratos entre archivos.
4. Elimina cualquier quorum/umbral de frecuencia; conserva todo hallazgo legítimo.
5. Deduplica por ubicación+categoría conservando severidad máxima.
6. Valida contra el checklist y reporta riesgos.

## Output

Devuelve el diseño en este shape: Markdown con summary, evidence, result, validation y
risks. Incluye un bloque de código GOOD del reviewer y, si aplica, el ANTI que reemplaza.
