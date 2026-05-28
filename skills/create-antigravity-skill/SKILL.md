---
name: create-antigravity-skill
description: >
  Constructor de skills de produccion. Genera skills estructuradas con SKILL.md + references/,
  validacion de calidad, y estandares canonicos. Usar cuando el usuario pida "crear skill",
  "nueva skill", "generar skill", "construir habilidad", o mencione skill architecture,
  skill scaffolding, o skill template generation. [EXPLICIT]
model: opus
context: fork
allowed-tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - Bash
version: 1.0.0
---

# Create Skill — Constructor de Skills de Produccion

Generar skills estructuradas, de alta densidad, listas para produccion. Cada skill sigue el
patron canonico: SKILL.md como orquestador + directorio `references/` con archivos de dominio
especificos. El constructor valida calidad antes de entregar. [EXPLICIT]

---

## Principio Rector

1. **Progressive Disclosure.** SKILL.md es el orquestador — contiene estructura, parametros, y flujo. La logica pesada vive en `references/`. Esto protege la ventana de contexto del agente y separa responsabilidades. [EXPLICIT]

2. **Densidad sobre verbosidad.** Cada linea del skill debe ser accionable. Sin platitudes genericas ("se util"), sin filler conversacional, sin repeticion. Si una instruccion no cambia el comportamiento del agente, sobra. [EXPLICIT]

3. **Validacion antes de entrega.** Ningun skill se entrega sin pasar el Validation Gate. El constructor verifica estructura, contenido, y coherencia antes de presentar al usuario. [EXPLICIT]

---

## Inputs

```
Parametros:
  MODO:     [piloto-auto | desatendido | supervisado | paso-a-paso]
  FORMATO:  [markdown | html | dual]
  ALCANCE:  [ejecutiva | tecnica]

Input requerido:
  - Nombre del skill (kebab-case)
  - Dominio / proposito funcional
  - Contexto: ¿que tipo de sistema o proyecto usara este skill?

Deteccion automatica:
  - Si el usuario describe un dominio tecnico → generar 3 reference files con nombres descriptivos
  - Si el usuario pide skill de auditoria → incluir PROFUNDIDAD en parametros del skill generado
  - Si el usuario menciona SAP/AWS/AI → adaptar cross-references al ecosistema correspondiente
  - Default: MODO=piloto-auto, FORMATO=markdown, ALCANCE=tecnica
```

Load references:

```
Read ${CLAUDE_SKILL_DIR}/references/skill-architecture-standard.md
Read ${CLAUDE_SKILL_DIR}/references/skill-quality-rubric.md
Read ${CLAUDE_SKILL_DIR}/references/skill-output-templates.md
```

---

## When to Use

- Crear un skill nuevo desde cero para cualquier dominio
- Generar la estructura de directorios y archivos para un skill
- Validar que un skill existente cumple el estandar canonico
- Refactorizar un skill que no sigue el patron de progressive disclosure

## When NOT to Use

- Auditar calidad de un skill existente en profundidad → usar x-ray-skill o certify-skill
- Disenar arquitectura de software (no skills) → usar el skill de dominio correspondiente
- Crear documentacion general (no skills) → escribir directamente

---

## Delivery Structure: 6 Sections

### S1: Analisis de Requisitos

Clarificar el nombre, proposito, dominio, y restricciones del skill solicitado. [EXPLICIT]

**Incluye:**
- Nombre en kebab-case
- Descripcion funcional con triggers de activacion
- Dominio tecnico y audiencia del skill
- Parametros que el skill generado necesitara
- Cross-references con skills existentes en el ecosistema

### S2: Generacion de Estructura

Crear la topologia de archivos siguiendo el patron canonico. [EXPLICIT]

**Estructura generada:**

```
{skill-name}/
├── SKILL.md                          # Orquestador
└── references/                       # Plural, siempre
    ├── {dominio}-{aspecto-1}.md      # Nombres descriptivos del dominio
    ├── {dominio}-{aspecto-2}.md
    └── {dominio}-{aspecto-3}.md
```

**Reglas de naming para references:**
- Nombres descriptivos del dominio, NO genericos (NO: knowledge_graph.md, best_practices.md)
- Kebab-case
- Prefijo del dominio para agrupacion (ej: aws-service-catalog.md, ai-quality-attributes.md)
- Minimo 3 archivos por skill

### S3: Generacion de SKILL.md

Generar el archivo orquestador con todas las secciones canonicas. [EXPLICIT]

**Secciones obligatorias del SKILL.md generado:**
1. Frontmatter YAML (name, description, model, context, allowed-tools)
2. Titulo + descripcion funcional
3. Principio Rector (2-3 reglas filosoficas del dominio)
4. Inputs (parametros + deteccion automatica + carga de referencias)
5. When to Use
6. When NOT to Use (con redireccion a skill correcto)
7. Delivery Structure: 6 Sections (S1-S6)
8. Trade-off Matrix
9. Assumptions
10. Limits
11. Edge Cases (3-5 escenarios)
12. Manejo de Inputs Ambiguos
13. Validation Gate (con nota de ejecutor)
14. Cross-References
15. Output Format Protocol
16. Output Artifact
17. Fuente (citaciones)

### S4: Generacion de Reference Files

Crear los 3+ archivos de referencia con contenido denso y especifico del dominio. [EXPLICIT]

**Cada reference file debe:**
- Contener la logica pesada que no debe estar en SKILL.md
- Usar tablas, listas, y diagramas Mermaid donde aporten claridad
- Ser auto-contenido (comprensible sin leer otros archivos)
- Seguir markdown linting estricto (blank lines alrededor de headings, listas, code fences)

### S5: Validacion de Calidad

Ejecutar el Validation Gate antes de entregar. [EXPLICIT]

**Checks obligatorios:**
- [ ] Frontmatter YAML completo y valido
- [ ] `references/` (plural) con minimo 3 archivos
- [ ] SKILL.md usa `${CLAUDE_SKILL_DIR}/references/` para cargar refs
- [ ] Todas las secciones canonicas presentes
- [ ] Sin platitudes genericas ni filler conversacional
- [ ] Nombres de reference files descriptivos del dominio
- [ ] Cross-references apuntan a skills existentes
- [ ] Markdown linting: blank lines alrededor de headings, listas, code fences
- [ ] Parametros usan taxonomia estandar (MODO, FORMATO, ALCANCE)
- [ ] Nota de ejecutor en Validation Gate del skill generado

### S6: Entrega y Documentacion

Presentar al usuario el skill generado con:
- Resumen de archivos creados
- Instrucciones de instalacion (copiar a directorio de skills)
- Sugerencias de mejora o extension

---

## Trade-off Matrix

| Decision | Habilita | Restringe | Cuando Usar |
|----------|----------|-----------|-------------|
| **3 refs minimo** | Separacion de responsabilidades, progressive disclosure | Mas archivos que mantener | Siempre — es el estandar |
| **Nombres descriptivos** | Encontrabilidad, claridad de proposito | No reutilizables entre skills | Siempre — nombres genericos confunden |
| **Todas las secciones** | Consistencia, completitud | Puede parecer excesivo para skills simples | Skills de produccion |
| **Frontmatter completo** | Deteccion automatica, routing correcto | Campos adicionales | Siempre — es el contrato |

---

## Assumptions

1. El usuario puede describir el dominio y proposito del skill con suficiente detalle
2. Existe un ecosistema de skills con estandares establecidos
3. Los skills generados seran ejecutados por agentes de IA con acceso a herramientas de archivo
4. El directorio de destino existe y es escribible

## Limits

1. NO genera skills que requieran herramientas no listadas en allowed-tools
2. NO crea contenido de dominio inventado — si el dominio es desconocido, solicita input del usuario
3. NO modifica skills existentes — solo crea nuevos (para modificar, usar surgeon-skill)
4. NO valida la ejecucion del skill — solo la estructura y contenido

---

## Edge Cases

1. **Dominio desconocido**: Si el usuario pide un skill para un dominio que el constructor no conoce, generar la estructura canonica con placeholders `[Requiere input del dominio: {descripcion}]` y solicitar contenido especifico. [EXPLICIT]

2. **Skill muy simple**: Si el dominio requiere menos de 6 secciones, mantener la estructura completa pero marcar secciones no aplicables como `[N/A para este dominio — {razon}]`. [EXPLICIT]

3. **Skill de auditoria**: Agregar automaticamente PROFUNDIDAD (express|standard|deep) a los parametros y separar de MODO (autonomia). [EXPLICIT]

4. **Skill que referencia otros inexistentes**: Documentar cross-references como `[Pendiente de construccion]` en lugar de omitirlas. [EXPLICIT]

5. **Usuario pide estructura legacy (4 archivos fijos)**: Migrar a la estructura canonica (3+ refs con nombres descriptivos). Documentar la migracion. [EXPLICIT]

---

## Manejo de Inputs Ambiguos

- Si el nombre del skill no se proporciona: solicitar antes de proceder.
- Si el dominio es vago ("hazme un skill de tecnologia"): pedir especificacion del subdominio y caso de uso concreto.
- Si el usuario no especifica MODO: usar `piloto-auto` (default).
- Si el usuario pide "un skill como X": analizar X como referencia y adaptar estructura, no copiar.
- Si el usuario quiere menos de 3 reference files: explicar el estandar y generar 3 minimo. Si insiste, documentar la desviacion.

---

## Validation Gate

*El agente que ejecuta este skill debe verificar cada item antes de entregar el output al usuario.*

- [ ] Estructura de directorios correcta ({skill-name}/ + SKILL.md + references/ + 3+ archivos)
- [ ] Frontmatter YAML del skill generado completo (name, description, model, context, allowed-tools)
- [ ] Todas las 17 secciones canonicas presentes en SKILL.md generado
- [ ] Reference files con nombres descriptivos del dominio (no genericos)
- [ ] Sintaxis de carga: `Read ${CLAUDE_SKILL_DIR}/references/{archivo}.md`
- [ ] Parametros usan taxonomia estandar (MODO, FORMATO, ALCANCE)
- [ ] Markdown linting: blank lines correctas, tablas alineadas, code fences separados
- [ ] Sin filler conversacional ni platitudes genericas
- [ ] Cross-references verificadas contra skills existentes
- [ ] Validation Gate del skill generado incluye nota de ejecutor

---

## Cross-References

| Skill | Relacion |
|-------|----------|
| Todos los skills del ecosistema | El constructor genera skills compatibles con el estandar de todos |
| `x-ray-skill` | Audita calidad de skills existentes — complementario |
| `surgeon-skill` | Mejora skills existentes — complementario |
| `certify-skill` | Certifica skills para produccion — downstream |

---

## Output Format Protocol

```
if FORMATO == "markdown":
  Archivos .md generados directamente en el directorio destino
  Resumen en consola con lista de archivos creados

if FORMATO == "html":
  Archivos .md generados + preview HTML del SKILL.md
  Audiencia: Revision visual antes de deploy

if FORMATO == "dual":
  Ambos formatos
```

## Output Artifact

```
{skill-name}/
├── SKILL.md
└── references/
    ├── {dominio}-{aspecto-1}.md
    ├── {dominio}-{aspecto-2}.md
    └── {dominio}-{aspecto-3}.md

Resumen de entrega:
  - Nombre: {skill-name}
  - Archivos generados: {N}
  - Secciones canonicas: 17/17
  - Reference files: {N} con nombres descriptivos
  - Validation Gate: PASS/FAIL
```

---

**Fuente**: Anthropic Skill Architecture Standards (2025). | Avila, R.D. & Ahmad, I. (2025). *Architecting AI Software Systems*. Packt.
