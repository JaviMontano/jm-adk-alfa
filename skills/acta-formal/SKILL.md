---
name: acta-formal
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Generates formal meeting records (actas) with legal/corporate format,
  numbered sections, signatures block, and branded HTML output. [EXPLICIT]
  Trigger: "acta formal", "formal minutes", "acta corporativa",
  "acta de junta", "acta de consejo", "acta con firmas", "quorum"
status: production
tags: [documents, meetings, formal, corporate, office]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__create_doc
  - mcp__workspace-mcp__modify_doc_text
  - mcp__workspace-mcp__create_drive_file
  - mcp__workspace-mcp__send_gmail_message
---

# Acta Formal

> "Lo que no se documenta, no existe." — Principio de gestion corporativa

## TL;DR

Genera borradores de actas formales de reunion con formato legal/corporativo: secciones numeradas, tabla de asistentes, quorum, acuerdos con responsables, bloque de firmas y salida markdown/HTML. No inventa acuerdos, quorum, folios, asistentes ni firmantes. La subida a Drive o envio por email requiere confirmacion humana explicita despues de revisar el borrador. [EXPLICIT]

## When to Activate

| Signal | Example |
|--------|---------|
| Acta formal | "Redacta el acta formal de la junta" |
| Acta corporativa | "Genera el acta de la reunion de consejo" |
| Formato legal | "Necesito las minutas en formato oficial" |
| Distribucion | "Crea el acta y mandala a los asistentes" |
| Firmas / quorum / folio | "Necesito acta con firmas, quorum y numero de folio" |

No activar para notas informales, resumen de standup o "acta de la reunion" sin senales formales; usar `meeting-notes`. Para preparar temas antes de la reunion, generar una agenda simple o derivar a una skill de agenda disponible; no referenciar una skill inexistente.

## S1 — Recopilar Metadata

1. **Datos generales**: fecha, hora inicio/fin, lugar (fisico o virtual), tipo de reunion
2. **Convocante**: nombre y cargo de quien convoca
3. **Asistentes**: nombre, cargo, firma (presente/ausente/justificado)
4. **Quorum**: validar que hay quorum suficiente para tomar acuerdos
5. **Numero de acta**: secuencial o por folio (integrar con `folio-generator` si disponible)

Si falta un dato critico, usar `por_confirmar` o pedirlo antes de cerrar el acta. No completar por inferencia nombres, cargos, asistentes, acuerdos, fechas limite, firmantes, quorum ni numero secuencial.

## S2 — Estructurar Acta

Secciones obligatorias (numeradas con romanos):

I. **Datos Generales** — Fecha, hora, lugar, tipo, numero de acta
II. **Lista de Asistencia y Quorum** — Tabla con nombre, cargo, asistencia, firma y estado de quorum
III. **Orden del Dia** — Puntos a tratar (numerados)
IV. **Desarrollo de la Sesion** — Resumen por punto del orden del dia
V. **Acuerdos** — Tabla: acuerdo, responsable, fecha limite, estado
VI. **Asuntos Varios** — Temas no incluidos en orden del dia
VII. **Cierre** — Hora de cierre, siguiente reunion programada
VIII. **Firmas** — Bloque de firmas del presidente y secretario

## S3 — Generar Output

1. Generar version markdown (para workspace)
2. Generar version HTML con estilo corporativo neutro o branded solo si existen tokens de marca
3. Si solicitado: preparar borrador para Google Doc via `create_doc`
4. Si solicitado: preparar subida a Drive via `create_drive_file` solo despues de confirmacion humana explicita
5. Si solicitado: preparar correo a asistentes via `send_gmail_message` solo despues de confirmacion humana explicita

## S4 — Validar

- [ ] Todas las secciones I-VIII presentes
- [ ] Quorum en estado `validado`, `no verificable` o `no aplica`
- [ ] Cada acuerdo tiene responsable y fecha limite
- [ ] Numero de acta es unico y secuencial, o queda `por_confirmar` si no hay fuente de folio
- [ ] Formato consistente (numeracion, tipografia)
- [ ] No hay asistentes, acuerdos, firmantes, folios o deadlines inventados
- [ ] Distribucion externa bloqueada hasta confirmacion humana explicita
- [ ] Evidence tags aplicados fuera del texto final del acta

## Quality Criteria

- [ ] Formato legal/corporativo valido
- [ ] Secciones numeradas con romanos (I-VIII)
- [ ] Tabla de asistentes completa
- [ ] Acuerdos con responsable y deadline
- [ ] Bloque de firmas al final
- [ ] Placeholders `por_confirmar` visibles para datos faltantes

## Anti-Patterns

- Generar acta sin validar quorum
- Omitir la seccion de acuerdos
- No numerar el acta secuencialmente
- Mezclar formato informal con formato de acta
- Inventar asistentes, firmantes, votos, quorum, folios o acuerdos
- Convertir pendientes o discusiones en acuerdos aprobados
- Enviar o subir el acta sin aprobacion humana explicita

## Related Skills

- `meeting-notes` — notas informales de reunion
- `follow-up-email` — enviar seguimiento post-reunion
- `folio-generator` — numeracion de documentos
- `office-workflow-runner` — orquestar borrador, revision y distribucion con gates

## Usage

- `/acta-formal` — generar acta completa
- "redacta el acta de la reunion de hoy"
- "genera el acta y mandala por email a todos"

## Assumptions & Limits

- Requiere input de la reunion (notas, transcript, o datos) [EXPLICIT]
- Formato latinoamericano corporativo por defecto [EXPLICIT]
- Numeracion secuencial requiere tracking manual o folio-generator [EXPLICIT]
