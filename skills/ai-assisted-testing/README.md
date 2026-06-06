# AI Assisted Testing

Generate deterministic, reviewable test plans and candidate test cases from code, requirements, defects, or risk areas. The skill covers unit tests, integration tests, property tests, fuzzing, mutation testing, regression tests, and coverage optimization.

Use this skill when the user asks for AI-generated tests, missing coverage analysis, fuzzing plan, mutation testing plan, test case generation, edge-case expansion, or coverage improvement.

## Deterministic Contract

- Every generated test must cite a target, rationale, oracle, and evidence source.
- Do not claim tests passed unless execution evidence is supplied.
- Fuzzing must be bounded: explicit input domain, seed policy, iteration limit, timeout, and safety boundary.
- Mutation testing must include baseline, mutation operators, surviving mutants, and kill criteria.
- Coverage optimization must identify target areas and thresholds instead of asking for vague "more tests."
- Machine-readable test plans must validate with `scripts/check.sh`.
