# Example Input

We need to update a JM Labs skill, run local validators, open a PR, and inspect GitHub Quality Gates. The user is currently in Codex with repo files available locally. There may be Claude and VS Code adapter docs in the repo, but no active authenticated Claude session is visible.

Produce a runtime-routing report that:

- compares Codex, Claude, VS Code, Gemini, Antigravity, and local adapter paths;
- cites repo files or executed checks for each supported capability;
- recommends the lowest-permission runtime that can edit files, run scripts, use `gh`, and preserve local git state;
- marks unverified runtime claims as validation pending;
- includes a local-first fallback if a remote runtime cannot be verified.
