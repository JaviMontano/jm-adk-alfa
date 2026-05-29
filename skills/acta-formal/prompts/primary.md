# Acta Formal Primary Prompt

## Objective

Generate a formal meeting record draft with sections I-VIII, quorum handling, agreements traceability, signatures, and safe distribution gates.

## Required Inputs

- Goal
- Context
- Constraints
- Definition of done
- Meeting metadata
- Attendees and attendance status
- Quorum threshold/source
- Agenda and discussion notes
- Explicit agreements with owner, deadline, and status
- President and secretary
- Requested output channels

## Process

1. Discover formal signals and route away to `meeting-notes` if the request is informal.
2. Extract only supplied facts; mark missing formal data `por_confirmar`.
3. Validate quorum as `validado`, `no verificable`, or `no aplica`.
4. Generate the acta body with sections I-VIII.
5. Separate agreements from pending items and discussions.
6. Produce validation notes outside the acta body.
7. Ask for explicit confirmation before Drive or Gmail distribution.

## Output

Return the acta in this shape: Datos Generales, Lista de Asistencia, Quorum, Orden del Dia, Desarrollo, Acuerdos, Asuntos Varios/Pendientes, Cierre, Firmas, and Validation Appendix.
