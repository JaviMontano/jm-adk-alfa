# Example Input

Start this session for `/Users/deonto/Documents/workspace/jm-adk-alfa`.

Context:

- Active brand: JM Labs.
- Current goal: continue the one-skill hardening queue.
- Required preflight:
  - `git status --short --branch`
  - `gh pr list --repo JaviMontano/jm-adk-alfa --state open --limit 30`
  - verify `main`, `origin/main`, `HEAD`, and remote `main` match
- Next skill: `session-start-bootstrap`.
- Stop if local changes or open PRs exist.

Return the start packet and first safe action.
