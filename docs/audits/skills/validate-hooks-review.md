# Skill Review: validate-hooks

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/validate-hooks`.
- [CODE] Review date: 2026-06-02.

## DoD Evidence

- [CODE] `assets/manifest.json` lists the local assets and validates asset consumers.
- [CODE] `assets/hooks-audit-schema.json` defines required structured audit fields.
- [CODE] `assets/hook-compatibility-matrix.json` defines all 22 events, all 4 hook types, and ToolUseContext compatibility.
- [CODE] `assets/command-safety-policy.json` defines offline command-string safety checks.
- [CODE] `assets/placement-guard-expectations.json` defines the expected PreToolUse placement guard.
- [CODE] `assets/validate-hooks-template.md` defines the stable Markdown report sections.
- [CODE] `scripts/compile-validate-hooks.py` compiles an offline hooks audit without executing hook commands or mutating config.
- [CODE] `scripts/check.sh` validates positive and negative fixtures for canonical shape, ToolUseContext incompatibility, command safety, and flat-array structure.
- [CODE] `scripts/fixtures/valid-hooks-audit-input.json` covers the passing canonical event-keyed shape.
- [CODE] `scripts/fixtures/invalid-tooluse-context.json` covers prompt/agent hooks on non-ToolUseContext events and a destructive command pattern.
- [CODE] `scripts/fixtures/invalid-flat-array-hooks.json` covers non-canonical flat-array structure.
- [CODE] `templates/output.md` and `templates/output.html` provide stable hooks audit output sections.
- [CODE] `evals/evals.json` contains concrete cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are domain-specific hooks audit examples.
- [CODE] `knowledge/body-of-knowledge.md` and `knowledge/knowledge-graph.*` document the offline audit contract.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill validate-hooks
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill validate-hooks
bash skills/validate-hooks/scripts/check.sh
python3 -B -m py_compile skills/validate-hooks/scripts/*.py
git diff --check
```

## Residual Limits

- [INFERENCE] This review certifies the `validate-hooks` skill only.
- [INFERENCE] Offline checks cannot prove runtime behavior of hook command bodies.
- [INFERENCE] Command safety checks are pattern-based and may miss project-specific hazards.
- [CODE] The compiler writes only a requested report path and never executes hook commands.
- [CODE] The shared `docs/audits/skill-review-ledger.csv` was intentionally not edited.
