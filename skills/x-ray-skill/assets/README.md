# x-ray-skill assets

This directory contains the deterministic scoring contract used by `x-ray-skill`.

## Files

- `manifest.json` lists every asset and its consumer.
- `rubric-policy.json` defines scoring dimensions, thresholds, and certification statuses.
- `gate-policy.json` defines the 13 binary quality checkpoints and component classifications.
- `report-template.md` documents the stable Markdown report sections.

The script in `../scripts/compile-x-ray-report.py` loads these assets and renders a repeatable scorecard from either a skill directory or a virtual fixture JSON.
