# Evals

## Purpose

Evals protect agentic behavior from regression. First-use onboarding has a root eval suite in `evals/onboarding/evals.json` and an executable smoke suite in `scripts/validate-onboarding.py`.

## Minimum Onboarding Cases

| ID | Case | Expected Behavior |
|---|---|---|
| `ONBOARDING-001` | greeting only | guided onboarding |
| `ONBOARDING-002` | empty input | no technical task starts |
| `ONBOARDING-003` | explicit task | micro-context then task |
| `ONBOARDING-004` | repo not confirmed | stop with `Dato requerido` |
| `ONBOARDING-005` | post-clone | safe first-use path |
| `ONBOARDING-006` | secret-like setup | reject or require placeholders |

## Command

```bash
python3 scripts/validate-onboarding.py
```
