<!--
generated-by: scripts/scaffold-skill.py
generated-for: git-hook-integration
generated-on: 2026-05-28
overwrite-policy: missing-only unless --force
-->

# Example Input

Create a plan-only Git hook integration for `jm-adk-alfa`.

Requirements:

- Use native Git hooks in `.githooks`.
- Add a fast `pre-commit` gate for repository guardrails and whitespace.
- Add a blocking `commit-msg` gate for Conventional Commits.
- Add a slower `pre-push` gate for component counts and strict skill validation.
- Do not install or overwrite hooks in this run.

Structured input lives at:

```text
skills/git-hook-integration/scripts/fixtures/git-hook-integration-input.json
```

Deterministic command:

```bash
python3 skills/git-hook-integration/scripts/compile-git-hook-integration.py \
  --input skills/git-hook-integration/scripts/fixtures/git-hook-integration-input.json
```
