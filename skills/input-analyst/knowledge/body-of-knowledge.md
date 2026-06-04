# Input Analyst — Body of Knowledge

## Canon

Input Analyst is a pre-processing skill. It improves raw user input before a
downstream skill acts. The canon is the five-pass pipeline:

1. Surface analysis: correct only objective errors and preserve meaning.
2. Five Whys: identify the root need with explicit, inferred, or open evidence.
3. Seven So-Whats: trace impact only until calibration is clear.
4. Intent gap analysis: classify vocabulary, scope, expertise, emotional, and
   context gaps.
5. Reformulation: produce a clarified prompt with constraints and open
   questions.

## Deterministic Contract

`scripts/compile-input-analysis.py` compiles an offline report from a local JSON
input. It uses:

- `assets/input-analysis-schema.json` for required fields and output sections.
- `assets/surface-patterns.json` for deterministic corrections and privacy
  signal checks.
- `assets/intent-gap-taxonomy.json` for gap detection and priority order.
- `assets/quality-calibration.json` for actionability, routing, quality level,
  and confidence thresholds.
- `assets/input-analysis-template.md` for canonical Markdown rendering.

The compiler must reject inputs that are empty or request non-offline routing.
It must not call external APIs, model providers, network resources, or MCP
tools.

## Output Schema

Required sections:

- `surface_errors`
- `five_whys`
- `seven_so_whats`
- `intent_gap_analysis`
- `ambiguity_register`
- `actionability_score`
- `clarified_prompt`
- `routing_hints`
- `user_safety_privacy_flags`
- `confidence`

## Quality Metrics
| Metric | Target | How to Measure |
|--------|--------|---------------|
| Surface preservation | 100% | Corrections never alter user intent |
| Evidence coverage | >= 80% | Claims tagged [CODE]/[INFERENCE]/[OPEN]/[DOC] |
| Actionability | >= 70 for execution | `actionability_score.score` |
| Ambiguity handling | 100% | Blocking context gaps route to clarification |
| Offline determinism | 100% | `scripts/check.sh` passes without network access |

## References
- `references/analysis-patterns.md`
- `references/five-whys-guide.md`
- `references/seven-so-whats-guide.md`
- `references/intent-detection.md`
- `assets/source-map.md`
