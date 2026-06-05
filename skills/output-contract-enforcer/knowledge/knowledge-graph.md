# Output Contract Enforcer - Knowledge Graph

## Core Concepts

- [[declared-contract]] - explicit rules the artifact must satisfy
- [[generated-artifact]] - output being validated
- [[validation-packet]] - pass/fail/blocked result with checks
- [[repair-suggestions]] - deterministic next edits
- [[evidence-tag-policy]] - allowed claim support vocabulary

## Relationships

```text
declared-contract + generated-artifact
├── format check
├── markdown section check
├── json required field check
├── evidence tag check
├── naming check
└── validation packet schema check

checks
├── pass -> proceed
├── fail -> repair required
└── blocked -> missing contract or artifact
```

## Routing Boundaries

- `structured-output`: design schemas or output formats before generation.
- `quality-gatekeeper`: make broader release decisions after contract validation.
- `prompt-creator`: generate durable prompt files.
