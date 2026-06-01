---
name: folio-generator
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Generates numbered business documents (folios) with auto-incrementing IDs,
  corporate branding, and tracking. For quotations, invoices, memos. [EXPLICIT]
  Trigger: "folio", "generar folio", "cotizacion", "numero de documento"
status: production
tags: [documents, numbering, tracking, corporate, office]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__create_doc
  - mcp__workspace-mcp__create_drive_file
  - mcp__workspace-mcp__send_gmail_message
---

# Folio Generator

> "Un documento sin numero es un documento perdido." — Principio de archivo

## TL;DR

Genera documentos numerados automaticamente con formato `{PREFIX}-{YYYY}-{NNN}`. Soporta cotizaciones (COT), memos (MEM), facturas (FAC), minutas (MIN), y tipos personalizados. Cada folio tiene numero unico, fecha, y contenido formateado. [EXPLICIT]

## When to Activate

| Signal | Example |
|--------|---------|
| Folio explicito | "Genera el folio para esta cotizacion" |
| Cotizacion | "Crea cotizacion COT-2026-001 para el cliente" |
| Documento numerado | "Necesito un memo numerado" |
| Factura | "Genera la factura FAC-2026-015" |

## S1 — Determinar Tipo y Numero

1. Identificar tipo de documento:
   - `COT` — Cotizacion / Presupuesto
   - `MEM` — Memorandum
   - `FAC` — Factura
   - `MIN` — Minuta / Acta
   - `DOC` — Documento generico
2. Ejecutar `scripts/next-folio-number.sh --dry-run --tracker .folio-tracker.json PREFIX` para calcular el siguiente numero sin mutar estado
3. Si el usuario confirma generacion/reserva, ejecutar `scripts/next-folio-number.sh --apply --tracker .folio-tracker.json PREFIX`
4. Si el usuario especifica numero, validar que no exista duplicado

## S2 — Generar Documento

1. Aplicar template con datos:
   - Folio ID en header
   - Fecha de emision
   - Destinatario / Cliente
   - Asunto
   - Cuerpo del documento
   - Pie con "Documento generado — Folio {ID}"
2. Usar `assets/folio-style.css` y `assets/brand-tokens.json` como fuente visual del HTML
3. Renderizar HTML con `scripts/render-folio-html.py --data <datos.json>` cuando existan datos estructurados
4. Generar version markdown

## S3 — Registrar y Distribuir

1. Actualizar `.folio-tracker.json` solo via `scripts/next-folio-number.sh --apply`
2. Si solicitado: crear en Google Docs via `create_doc`
3. Si solicitado: subir a Drive via `create_drive_file`
4. Si solicitado: enviar por email via `send_gmail_message`

## S4 — Validar

- [ ] Numero de folio es unico
- [ ] Formato PREFIX-YYYY-NNN correcto
- [ ] Tracker actualizado
- [ ] Documento tiene todas las secciones

## Folio Format Rules

| Prefijo | Tipo | Ejemplo |
|---------|------|---------|
| COT | Cotizacion | COT-2026-001 |
| MEM | Memorandum | MEM-2026-015 |
| FAC | Factura | FAC-2026-042 |
| MIN | Minuta | MIN-2026-003 |
| DOC | Generico | DOC-2026-100 |

## Quality Criteria

- [ ] Numero unico, sin duplicados
- [ ] Formato consistente (PREFIX-YYYY-NNN)
- [ ] Dry-run no muta `.folio-tracker.json`
- [ ] Tracker actualizado despues de cada generacion confirmada
- [ ] Template aplicado correctamente

## Anti-Patterns

- Generar folios sin actualizar el tracker
- Permitir numeros duplicados
- Usar formato inconsistente entre documentos
- Editar `.folio-tracker.json` con grep/sed o texto ad hoc

## Deterministic Script Contract

- Runtime script: `scripts/next-folio-number.sh`
- Rendering script: `scripts/render-folio-html.py`
- Contract check: `scripts/check.sh`
- Validation command: `python3 scripts/validate-skill-scripts.py --strict --run-checks`
- Default behavior: `--dry-run` prints the next folio without creating or mutating the tracker.

## Assets Contract

- Visual assets live in `assets/`.
- `assets/manifest.json` lists every output asset and where it is used.
- `assets/folio-style.css` is the print-safe stylesheet for HTML folios.
- `assets/brand-tokens.json` carries the default neutral business design tokens.

## Related Skills

- `acta-formal` — actas numeradas con folio
- `invoice-generator` — facturas (puede usar folio)
- `proposal-writing` — cotizaciones con folio

## Usage

- `/folio-generator` — generar documento numerado
- "genera folio COT-2026 para la cotizacion del cliente X"
- "crea un memo numerado sobre el cambio de politica"
