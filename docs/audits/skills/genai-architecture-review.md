# Skill Review: genai-architecture

## Verdict

- [CODE] Status: `dod-complete`.
- [CODE] Scope: one skill only, `skills/genai-architecture`.
- [CODE] Review date: 2026-06-01.

## DoD Evidence

- [CODE] `assets/manifest.json` lists every local asset and validates asset consumers.
- [CODE] `assets/genai-architecture-schema.json` defines the structured input contract.
- [CODE] `assets/rag-pattern-model.json` defines RAG variants, stages, retrieval methods, and chunking strategies.
- [CODE] `assets/model-routing-matrix.json` defines LLM tiers, routing criteria, and fallback controls.
- [CODE] `assets/vector-db-selection-matrix.json` defines deterministic vector store recommendation rules.
- [CODE] `assets/connector-security-model.json` defines connector controls and degraded behaviors.
- [CODE] `assets/qa-metrics-model.json` defines GenAI metrics, guardrails, and improvement cadence.
- [CODE] `scripts/compile-genai-architecture.py` compiles structured JSON into Markdown without network access.
- [CODE] `scripts/check.sh` validates JSON fixtures, required report fragments, and invalid-input failure.
- [CODE] `evals/evals.json` contains concrete cases with `assets`, `deterministic_scripts`, and `quality_criteria` checks.
- [CODE] `examples/example-input.md` and `examples/example-output.md` are domain-specific, not scaffold placeholders.

## Validation Commands

```bash
python3 -B scripts/validate-skill-dod.py --skill genai-architecture
python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill genai-architecture
bash skills/genai-architecture/scripts/check.sh
```

## Residual Limits

- [INFERENCE] This review certifies the `genai-architecture` skill only.
- [INFERENCE] It does not imply the remaining pending catalog skills are DoD-complete.
