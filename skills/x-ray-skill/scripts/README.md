# x-ray-skill scripts

## compile-x-ray-report.py

Reads a real skill directory or a virtual fixture JSON and renders a deterministic X-Ray scorecard.

```bash
python3 skills/x-ray-skill/scripts/compile-x-ray-report.py \
  --skill-dir skills/x-ray-skill \
  --format markdown
```

Fixture mode is used by `check.sh` for deterministic positive and negative cases:

```bash
python3 skills/x-ray-skill/scripts/compile-x-ray-report.py \
  --fixture skills/x-ray-skill/scripts/fixtures/certified-skill.json \
  --format json
```

The script is read-only. It never edits the audited skill.
