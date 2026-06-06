# Example Input

Before compaction, preserve the current state for the next session.

Context:

- Active brand: JM Labs.
- Active repo: `/Users/deonto/Documents/workspace/jm-adk-alfa`.
- Active branch: `codex/harden-pre-compact-context-dod-20260606`.
- Rule: exactly one skill, one branch, one PR, one green merge at a time.
- Current skill: `pre-compact-context`.
- Completed locally: assets, evals, examples, prompts, templates, knowledge, and
  scripts were updated.
- Validations to preserve:
  - `python3 -B scripts/validate-skill-dod.py --skill pre-compact-context`
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill pre-compact-context`
  - `bash skills/pre-compact-context/scripts/check.sh`
- Open risk: PR is not opened yet.

Return a compact packet that the next session can use to resume without reading
the full conversation.
