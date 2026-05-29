# Acta Formal

Genera borradores de actas corporativas con estructura formal, quorum, folio, asistentes, acuerdos, responsables, fechas, firmas y salida Markdown/HTML. Protege contra datos inventados y contra distribucion externa sin aprobacion.

## Triggers

- "acta formal"
- "acta corporativa"
- "acta de junta"
- "acta de consejo"
- "acta con firmas"
- "quorum"
- "formal minutes"
- "formato oficial de reunion"

## Allowed Tools

- Read
- Write
- Bash
- mcp__workspace-mcp__create_doc
- mcp__workspace-mcp__modify_doc_text
- mcp__workspace-mcp__create_drive_file
- mcp__workspace-mcp__send_gmail_message

## Quick Use

Use this skill when the user needs a formal record, not quick meeting notes. The request should include or imply formal signals: quorum, folio, signatures, junta, consejo, asamblea, committee, official minutes, or corporate/legal format.

Minimum useful input:

- date, start/end time, location or virtual channel;
- meeting type, convener, president and secretary;
- invited and attendee list with attendance status;
- quorum threshold or source, or permission to mark it `por_confirmar`;
- agenda items and discussion notes;
- explicit agreements, each with responsible person, deadline and status;
- desired outputs: Markdown, HTML, Google Doc draft, Drive upload, or email draft.

If the request is only "take notes" or "acta de la reunion de hoy" without formal signals, route to `meeting-notes`.

## Output Format

Acta formal with:

- I. Datos Generales;
- II. Lista de Asistencia and Quorum;
- III. Orden del Dia;
- IV. Desarrollo de la Sesion;
- V. Acuerdos;
- VI. Asuntos Varios;
- VII. Cierre;
- VIII. Firmas;
- validation notes outside the final acta.

External distribution is draft-only until the user explicitly confirms upload or email.
