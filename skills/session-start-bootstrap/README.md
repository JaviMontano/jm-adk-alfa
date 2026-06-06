# Session Start Bootstrap

`session-start-bootstrap` creates a deterministic start packet before an agent
does work. It verifies environment, loads minimal relevant context, initializes
guardrails, records blockers, and names the first safe action.

## Triggers

- `session start bootstrap`
- `/session-start-bootstrap`
- `start this session`
- `bootstrap the repo`
- `resume from handoff`

Do not activate for generic project summaries or implementation requests unless
the session needs an explicit startup gate.

## Resources

- `assets/bootstrap-contract.json` - required packet structure.
- `assets/environment-policy.json` - repo/branch/PR/dirty-tree checks.
- `assets/context-loading-policy.json` - minimal context loading rules.
- `assets/guardrails-policy.json` - hard rules and stop conditions.
- `assets/source-priority.json` - precedence for conflicting sources.
- `scripts/check.sh` - offline fixture validation.

## Required Output

1. Environment
2. Context Sources Loaded
3. Active Guardrails
4. Current State
5. Blockers And Gaps
6. Validation Baseline
7. First Action
8. Guardian Decision

## Validation

```bash
bash skills/session-start-bootstrap/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-start-bootstrap
python3 -B scripts/validate-skill-dod.py --skill session-start-bootstrap
```

## Safety Rules

- Never start writes from a dirty tree without explicit scope resolution.
- Never assume PR/CI/merge state without evidence.
- Load only task-relevant context.
- Preserve hard rules exactly.
