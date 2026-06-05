# Skill Review: user-prompt-filter

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/user-prompt-filter`.
- [CONFIG] Review date: 2026-06-02.
- [CONFIG] The full ledger row is kept deferred from this PR to avoid the
  large-file transport risk already observed during granular deployments.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates each
  consumer path.
- [CODE] `assets/filter-input-schema.json` defines the required prompt filter
  input fields.
- [CODE] `assets/threat-taxonomy.json` defines prompt injection, tool override,
  secret exfiltration, protected context leakage, destructive action, ambiguous
  authority, and benign controls.
- [CODE] `assets/risk-scoring-policy.json` maps matched threats to severity,
  confidence, and routing decisions.
- [CODE] `assets/sanitization-policy.json` defines unsafe text removal,
  protected-term redaction, and downstream constraints.
- [CODE] `assets/output-schema.json` defines the deterministic report shape.
- [CODE] `scripts/filter-prompt.py` validates local JSON and renders Markdown
  or stable JSON offline without APIs, network, MCP, browser, or tool calls.
- [CODE] `scripts/check.sh` validates prompt injection, benign summary, secret
  exfiltration, ambiguous authority, and invalid input fixtures.
- [CODE] `evals/evals.json` includes eight concrete cases with `assets`,
  `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are
  domain-specific and do not retain scaffold placeholders.
- [CODE] Roles, prompts, knowledge graph, README, and reference docs now
  describe pre-execution prompt filtering instead of generic skill scaffolding.

## Validation Commands

```text
bash skills/user-prompt-filter/scripts/check.sh
user-prompt-filter fixtures passed

python3 -B scripts/validate-skill-dod.py --skill user-prompt-filter
PASS user-prompt-filter: user-prompt-filter fixtures passed
skills_with_scripts=1 warnings=0 errors=0
skill=user-prompt-filter dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill user-prompt-filter
PASS user-prompt-filter: user-prompt-filter fixtures passed
skills_with_scripts=1 warnings=0 errors=0

python3 -B -m py_compile skills/user-prompt-filter/scripts/*.py
PASS
```

## Residual Limits

- [INFERENCE] Offline prompt filtering does not enforce runtime permissions,
  filesystem sandboxing, network limits, or human approvals.
- [INFERENCE] Pattern-based detection can miss novel attacks; runtime defense
  in depth remains required.
- [INFERENCE] The filter intentionally escalates ambiguous authority instead of
  treating claimed authorization as proof.
