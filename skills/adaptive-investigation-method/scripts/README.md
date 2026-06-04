# adaptive-investigation-method scripts

## `compile-adaptive-investigation.py`

Validates an adaptive investigation loop spec and renders a deterministic Markdown or JSON report.

```bash
python3 skills/adaptive-investigation-method/scripts/compile-adaptive-investigation.py \
  --input skills/adaptive-investigation-method/scripts/fixtures/auth-repo-investigation.json \
  --format markdown
```

The compiler is read-only. It rejects missing budgets, expensive reads beyond budget, non-cheap mapping, unlinked hypotheses, reflexive replans, invalid stop conditions, and anti-pattern tokens.

## `check.sh`

Runs JSON validation, Python syntax validation, positive fixture rendering, expected fragment checks, and negative fixture checks.
