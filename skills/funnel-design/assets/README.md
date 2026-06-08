# Funnel Design Assets

Local assets convert funnel design from a prompt-only workflow into a deterministic blueprint.

## Files

- `manifest.json` - inventory consumed by the DoD validator.
- `funnel-design-schema.json` - required structured input contract.
- `stage-content-model.json` - TOFU/MOFU/BOFU stage requirements.
- `lead-scoring-model.json` - scoring dimensions and lifecycle thresholds.
- `nurture-flow-schema.json` - trigger, delay, branch, message, and exit requirements.
- `qualification-rules.json` - sales-ready and disqualification rules.
- `funnel-design-report-template.md` - Markdown template rendered by the compiler.

## Runtime

Run `scripts/check.sh` to validate JSON assets, fixtures, deterministic output fragments, and invalid-input behavior.
