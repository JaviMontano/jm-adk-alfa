# Example Input

Create a dry-run workspace setup plan for JM Labs in Codex.

- goal: harden one skill at a time with PR-based evidence
- runtime: Codex
- autonomy: implement after local preflight is clean
- allowed commands: `git status --short --branch`, `python3 -B scripts/validate-skills.py --strict`
- prohibited commands: `git reset --hard`, `rm -rf`
- privacy: local-only profile, no secrets, redact tokens and email addresses
- output format: Markdown with evidence tags
- target file: `.jm-adk.local.json`
