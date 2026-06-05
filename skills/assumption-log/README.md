# Assumption Log

Deterministic assumption tracking for project decisions.

Use this skill when a project needs to identify, preserve, validate, invalidate,
or retire assumptions before planning or delivery. The output is a register with
stable `A-NNN` IDs, allowed statuses, evidence tags, contradiction links,
decision links, and a validation queue.

## Local Resources

- `assets/activation-policy.json`: activation and false-positive routing
- `assets/status-policy.json`: ID, status, impact, risk, and transition policy
- `assets/log-contract.json`: required report sections and fields
- `assets/evidence-policy.json`: evidence tags and proof requirements
- `scripts/validate_assumption_log.py`: offline report validator
- `scripts/check.sh`: deterministic fixture test

## Local Checks

```bash
bash skills/assumption-log/scripts/check.sh
python3 -B scripts/validate-skill-dod.py --skill assumption-log
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill assumption-log
```

## Decision Rule

Validated and invalidated assumptions require strong evidence. Open
high-impact assumptions must stay visible in the validation queue until closed.
