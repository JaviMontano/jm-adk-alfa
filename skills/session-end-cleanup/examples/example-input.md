# Example Input

Run session end cleanup for the `codex/harden-session-end-cleanup-dod-20260606`
branch.

Context:

- Active brand: JM Labs.
- Active repo: `/Users/deonto/Documents/workspace/jm-adk-alfa`.
- Completed work: specialized `session-end-cleanup` assets, evals, examples,
  prompts, templates, knowledge, and scripts.
- Commands run:
  - `python3 -B scripts/validate-skill-dod.py --skill session-end-cleanup`
  - `python3 -B scripts/validate-skill-scripts.py --strict --run-checks --skill session-end-cleanup`
  - `bash skills/session-end-cleanup/scripts/check.sh`
  - `python3 -B scripts/validate-skills.py --strict`
- PR state: not opened yet.
- Durable updates allowed: update the session-end-cleanup review doc and ledger
  row only after validation passes.

Return the closeout packet and block if any validation or PR evidence is
missing.
