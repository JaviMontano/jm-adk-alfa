# Acta Formal Body of Knowledge

## Canon

An acta formal is a corporate record. Its value depends on fidelity to the meeting inputs and on clear separation between facts, assumptions, pending data, and external distribution. The skill drafts the acta; it does not certify legal validity unless the user supplies the governing rules and confirms review.

## Hard Rules

- Do not invent attendees, absences, votes, agreements, deadlines, folio numbers, president, secretary, or signatures.
- Use `por_confirmar` for missing critical fields when the user cannot provide them in the current turn.
- Quorum must be one of `validado`, `no verificable`, or `no aplica`.
- If quorum is `no verificable` or not reached, do not present agreements as binding. Record them as discussion items or pending confirmation.
- A pending action is not an agreement unless the input says it was approved or agreed.
- Distribution through Drive or Gmail requires explicit human confirmation after draft review.
- Evidence and validation notes must stay outside the final acta body.

## Required Inputs

| Field | Required | Fallback |
| --- | --- | --- |
| Acta number / folio | Yes for final | `por_confirmar` if no source of sequence exists |
| Date and start/end time | Yes | `por_confirmar` |
| Location or virtual channel | Yes | `por_confirmar` |
| Meeting type | Yes | `por_confirmar` |
| Convener | Yes | `por_confirmar` |
| Attendees and attendance state | Yes | `por_confirmar` rows |
| Quorum threshold/source | Required when agreements are binding | `no verificable` |
| Agenda | Preferred | State no formal agenda was provided |
| Discussion notes | Yes | Summarize only supplied facts |
| Agreements | Only if explicitly agreed | Use pending items otherwise |
| President and secretary | Required for signatures | `por_confirmar` |

## Output Contract

The final acta body must include:

1. Datos Generales
2. Lista de Asistencia
3. Quorum
4. Orden del Dia
5. Desarrollo de la Sesion
6. Acuerdos
7. Asuntos Varios
8. Cierre
9. Firmas

The validation appendix should include missing fields, assumptions, quorum status, distribution status, and no-invention confirmation.

## Quality Signals

| Signal | Target |
|---|---|
| Evidence coverage | Claims are grounded or marked as assumptions |
| Scope control | Output stays inside the requested domain |
| Update safety | Existing manual work is preserved |
| No-invention | Formal facts come only from supplied input or are `por_confirmar` |
| Quorum safety | Binding agreements appear only when quorum is validated or not applicable |
| Distribution gate | External send/upload waits for explicit confirmation |

## Open Knowledge

- Add organization-specific statutes, quorum thresholds, signature rules, numbering conventions, and brand tokens only when they become stable sources.
