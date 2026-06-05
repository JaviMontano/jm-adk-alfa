# workflow-forge review

## Decision

[CODE] `workflow-forge` is DoD-ready in this prepared patch.

## Evidence

- [CODE] `skills/workflow-forge/assets/` defines the schema, workflow policy,
  Markdown output template, source map, and manifest.
- [CODE] `skills/workflow-forge/scripts/compile-workflow-forge.py` validates a
  structured workflow spec and renders deterministic Markdown or JSON without
  network, MCP, model, or API calls.
- [CODE] `skills/workflow-forge/scripts/check.sh` validates positive Markdown
  and JSON output plus negative fail-closed fixtures for single-phase workflows,
  missing verification, and prohibited stack terms.
- [CODE] `skills/workflow-forge/evals/evals.json` now covers activation,
  compiler behavior, negative fixtures, unresolved references, and routing false
  positives.

## Gates

```text
python3 -B scripts/validate-skill-dod.py --skill workflow-forge
PASS workflow-forge: OK: workflow-forge scripts are deterministic
skills_with_scripts=1 warnings=0 errors=0
skill=workflow-forge dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-forge
PASS workflow-forge: OK: workflow-forge scripts are deterministic
skills_with_scripts=1 warnings=0 errors=0

bash skills/workflow-forge/scripts/check.sh
OK: workflow-forge scripts are deterministic

python3 -B scripts/validate-skills.py --strict
skills=585 warnings=0 errors=0

python3 -B scripts/count-components.py --check-docs
skills=585
agents=260
commands=267
prompts=256
components=1368

bash scripts/check-repo-boundaries.sh
Repo boundaries OK

python3 -B scripts/validate-skill-scripts.py --strict --run-checks
skills_with_scripts=19 warnings=0 errors=0

python3 -B scripts/qa/run-adversarial-tests.py
summary: passed=11 failed=0 total=11

bash -n skills/workflow-forge/scripts/check.sh
PASS

python3 -B -m py_compile skills/workflow-forge/scripts/compile-workflow-forge.py
PASS

git diff --check
PASS

git diff --check -- skills/workflow-forge docs/audits/skills/workflow-forge-review.md
PASS
```

## Limits

- [INFERENCE] The compiler validates workflow structure and policy compliance;
  it does not prove the generated workflow is strategically correct.
- [INFERENCE] Catalog integrity still depends on the available local agent and
  skill indexes; unknown references should remain `[OPEN]`.
- [INFERENCE] The skill creates workflow definitions; it does not execute the
  workflow itself.

## Ledger Completion 2026-06-05

- [CODE] `bash skills/workflow-forge/scripts/check.sh` passed in `codex/complete-script-backed-ledger-20260605` validation.
- [CODE] `python3 -B scripts/validate-skill-dod.py --skill workflow-forge` passed with `skill=workflow-forge dod=pass errors=0`.
- [CODE] `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill workflow-forge` passed with `skills_with_scripts=1 warnings=0 errors=0`.
- [CONFIG] `docs/audits/skill-review-ledger.csv` now records `workflow-forge` as `dod-complete`.
