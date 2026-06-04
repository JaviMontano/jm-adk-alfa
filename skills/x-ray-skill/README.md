# X-Ray Skill

`x-ray-skill` audits a skill directory and produces a scorecard against the gold-standard anatomy and 10-dimension quality rubric.

## Inputs

- Path to a skill directory that contains `SKILL.md`.
- Optional virtual fixture JSON for deterministic tests.
- Reference rubric files under `references/`.

## Output

A Markdown or JSON X-Ray report with summary, rubric scores, 13 gate results, top issues, component classification, and recommended next step.

## Deterministic Script

```bash
python3 skills/x-ray-skill/scripts/compile-x-ray-report.py \
  --skill-dir skills/x-ray-skill \
  --format markdown
```

Run `bash skills/x-ray-skill/scripts/check.sh` to verify fixture scoring, invalid input rejection, and self-audit rendering.
