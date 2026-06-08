# Cv Cover Optimizer Scripts

`ats_lint.py` validates JSON CV/cover packets offline.

## Contract

- No network access.
- No wall-clock or random dependency.
- Valid fixtures must pass.
- Invalid fixtures must fail.
- The linter reports issues instead of rewriting files.

## Validate

```bash
bash skills/cv-cover-optimizer/scripts/check.sh
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill cv-cover-optimizer
```
