# Scripting And Bash

## Purpose

Alfa scripts should be safe to run in local developer environments and clear about the files they may touch.

## Script Rules

- Detect repo root with `git rev-parse --show-toplevel` or an equivalent `git -C` lookup.
- Use dry-run by default when a script may create, move, or write many files.
- Require `--apply` or an equally explicit flag for writes.
- Require `--force` for overwrites.
- Never read, print, or store `.env*`, credentials, tokens, keys, or private secrets.
- Avoid destructive commands such as hard resets, broad deletes, or force pushes.
- Print clear status and exit nonzero on blocking errors.

## Skill Script Contract

When a skill owns local automation under `skills/<skill>/scripts/`, it must include:

- `scripts/README.md` with entry points, state files, and mutation rules.
- `scripts/check.sh` as the deterministic runtime smoke test.
- `scripts/fixtures/*.json` for stable inputs and expected outputs.
- A `SKILL.md` reference to `scripts/` or the script entry point.

Skill scripts must remain non-destructive by default. Any write to workspace state must require `--apply` or an equally explicit flag.

## User Context Scripts

`scripts/diagnose-user-context.py` is read-only. It identifies the in-kit
context repo by `user-context/.jm-adk-context.json` and reports marker,
location, manifest, tracked-private-file, and secret-like autoload issues.

`scripts/scaffold-user-context.py` is dry-run first and writes only with
`--apply`. It creates or repairs the scaffold; private user content remains
ignored by git.

## Runtime Instruction Validation

`scripts/validate-runtime-instructions.py` is read-only. It verifies that
`CLAUDE.md`, `GEMINI.md`, `AGENTS.md`, and adapter bridge files share the
runtime context contract, reject stale `constitution-v5.2.0` references, and
preserve the `user-context/` boundary.

## Validation

Use:

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/*.sh scripts/adapters/*.sh
python3 scripts/validate-skill-scripts.py --strict --run-checks
python3 scripts/validate-runtime-instructions.py
```

Run behavior-specific smoke tests before handoff.
