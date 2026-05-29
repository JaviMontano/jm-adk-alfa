---
description: "Validate Alfa first-use onboarding, repo confirmation, explicit-task handling, and setup safety."
user-invocable: true
---

# /jm-adk:validate-onboarding

## Purpose

Run the non-destructive onboarding regression suite.

## Command

```bash
python3 scripts/validate-onboarding.py
```

## Covered Cases

- Greeting-only input activates onboarding.
- Empty input does not start technical work.
- Explicit task uses micro-context and proceeds.
- Non-Alfa repo stops with `Dato requerido`.
- Setup writes only with `--apply`.
- Secret-like profile inputs are rejected.
