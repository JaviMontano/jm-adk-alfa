# Example Output

## Summary

- Component type: `hook` [EXPLICIT]
- Recommended name: `handoff-packet-check` [EXPLICIT]
- Source mode: plugin brief with named existing components [EXPLICIT]

## Candidates

| Name | Responsibility | Rationale |
|------|----------------|-----------|
| `handoff-packet-check` | This hook validates session handoff packets against required closeout sections. | Best fit because it names the lifecycle artifact and validation scope. [INFERRED] |
| `session-handoff-audit` | This hook audits session handoff completeness after session close. | Clear, but broader than the requested packet check. [INFERRED] |

## Relationships

- Direct dependencies: `session-end-cleanup` produces the packet; `quality-gatekeeper` owns validation patterns. [EXPLICIT]
- Downstream consumers: session resume workflows and human reviewers. [INFERRED]
- Hook compatibility: `type:command` with `Stop` event. [EXPLICIT]
- Diagram: `session-end-cleanup -> handoff-packet-check -> quality-gatekeeper`. [INFERRED]

## Conflict Analysis

- Status: `overlap` with `quality-gatekeeper` validation responsibility. [INFERRED]
- Resolution: `differentiate`; the hook checks closeout packet structure only, while `quality-gatekeeper` remains the general validation authority. [INFERRED]

## MOAT Depth

- Level: `FULL`. [INFERRED]
- Required assets: `SKILL.md`, `references/`, `examples/`. [INFERRED]
- Rationale: lifecycle hook behavior needs compatibility reference and examples for pass/fail packet shapes. [INFERRED]

## Tools and Size

- Tools needed: `Read`, `Grep`, `Bash` for deterministic local packet validation. [INFERRED]
- Estimated lines: `14-24`. [INFERRED]

## Validation

- PASS: component type is valid, name is kebab-case, and hook event is compatible. [INFERRED]
- PASS: conflict status includes a resolution. [INFERRED]

## Risks

- The plugin brief did not include the actual hooks registry, so compatibility is based on the supplied event and local policy matrix. [SUPUESTO]
