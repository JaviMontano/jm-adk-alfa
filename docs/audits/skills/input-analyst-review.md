# input-analyst review

## Decision

[CODE] `input-analyst` is `dod-complete` for the deterministic skill contract.

## Evidence

- [CODE] The skill includes complete core files, `assets/`, deterministic
  `scripts/`, fixtures, examples, evals, templates, knowledge, prompts, and
  agent files.
- [CODE] `scripts/compile-input-analysis.py` compiles a stable offline analysis
  with surface errors, 5 Whys, 7 So-Whats, intent gap analysis, ambiguity
  register, actionability score, clarified prompt, routing hints, user
  safety/privacy flags, and confidence.
- [CODE] The compiler rejects empty input and rejects routing policies that allow
  external APIs or disable offline-only execution.
- [DOC] Local references used: `analysis-patterns.md`, `five-whys-guide.md`,
  `intent-detection.md`, and `seven-so-whats-guide.md`.

## Checks

```text
python3 -B scripts/validate-skill-dod.py --skill input-analyst
skill=input-analyst dod=pass errors=0

python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill input-analyst
PASS input-analyst: OK: input-analyst scripts are deterministic and offline
skills_with_scripts=1 warnings=0 errors=0

bash skills/input-analyst/scripts/check.sh
OK: input-analyst scripts are deterministic and offline

python3 -B -m py_compile skills/input-analyst/scripts/*.py
PASS

git diff --check
skills/validate-hooks/examples/example-input.md:46: new blank line at EOF.
skills/validate-hooks/examples/example-output.md:63: new blank line at EOF.
skills/validate-hooks/templates/output.docx.md:21: new blank line at EOF.
skills/validate-hooks/templates/output.html:156: new blank line at EOF.
skills/validate-hooks/templates/output.md:51: new blank line at EOF.

git diff --check -- skills/input-analyst docs/audits/skills/input-analyst-review.md
PASS
```

## Residual Limits

[INFERENCE] Offline heuristic analysis cannot prove the user's true intent. It
only creates a grounded hypothesis, surfaces ambiguities, and routes low-context
requests to clarification before downstream execution.

[INFERENCE] Privacy flags are deterministic pattern matches. They catch common
email, phone-like, and secret-keyword signals, but they are not a full DLP
system.

[INFERENCE] The full-worktree whitespace check currently fails because of
`skills/validate-hooks/**`, which is outside this review's ownership boundary.
The scoped whitespace check for `input-analyst` and its review passes.
