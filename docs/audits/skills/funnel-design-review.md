# Skill Review: funnel-design

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/funnel-design`.
- [CODE] Review date: 2026-06-01.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/funnel-design-schema.json` defines the structured input contract.
- [CODE] `assets/stage-content-model.json` defines TOFU/MOFU/BOFU stage requirements.
- [CODE] `assets/lead-scoring-model.json` defines deterministic scoring thresholds.
- [CODE] `assets/nurture-flow-schema.json` defines trigger, delay, branch, and exit requirements.
- [CODE] `scripts/compile-funnel-design.py` compiles structured JSON into Markdown without network access.
- [CODE] `scripts/check.sh` validates JSON fixtures, required report fragments, and invalid-input failure.
- [CODE] `evals/evals.json` contains 9 concrete cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are domain-specific, not scaffold placeholders.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill funnel-design
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill funnel-design
bash skills/funnel-design/scripts/check.sh
```

## Residual Limits

- [INFERENCE] This review certifies the `funnel-design` skill only.
- [INFERENCE] It does not imply the remaining pending catalog skills are DoD-complete.
