# Example Output

## Reference Packet

- As of: `2026-06-08` [EXPLICIT]
- Packet status: `blocked` [INFERRED]
- Validation: `blocked` [EXPLICIT]

## Contacts

| ID | Label | Relationship | Consent | Allowed actions | Evidence |
| --- | --- | --- | --- | --- | --- |
| C-001 | Ana Gomez | Former delivery stakeholder | explicit_granted | list_reference, recruiter_contact | E-001 |
| C-002 | Luis Perez | Former delivery collaborator | not_requested | none | E-002 |

## Actions

| ID | Contact | Action | Due | Evidence |
| --- | --- | --- | --- | --- |
| A-001 | C-002 | request_consent | 2026-06-10 | E-002 |

## Blockers

- `C-002` cannot be listed or contacted until explicit consent is recorded. [EXPLICIT]

## Validation Notes

- Direct contact details omitted. [EXPLICIT]
- Follow-up cadence computed from `as_of`, not current time. [EXPLICIT]
