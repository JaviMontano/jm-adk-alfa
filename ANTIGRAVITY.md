# ANTIGRAVITY.md

## Purpose

Alfa exposes an Antigravity-compatible derived view through `.agent/` and `scripts/adapters/antigravity.sh`. Antigravity belongs to the GEMINI runtime family: `GEMINI.md` is the homologated mirror, and `.agent/rules/GEMINI.md` is the Antigravity bridge. Runtime capability claims remain validation pending until tested in the target Antigravity environment.

## First Use

1. Confirm this repo is Alfa before edits.
2. Run `python3 scripts/diagnose-first-use.py --dry-run`.
3. Run `python3 scripts/diagnose-user-context.py --dry-run` before relying on durable user context.
4. Use `/jm-adk:first-use` for greeting-only or empty input.
5. Use `/jm-adk:start-task` for explicit tasks.
6. Fall back to Markdown-first instructions when runtime support is unclear.

## Generated View

- `.agent/skills_index.json` indexes root skills.
- `.agent/rules/GEMINI.md` contains the generated Antigravity bridge for the GEMINI mirror.
- `.agent/ARCHITECTURE.md` mirrors current architecture counts where supported.

## Boundaries

- Do not assume hooks, MCP, workspace management, function calling, or multimodal support unless validated in the runtime.
- Do not route secrets through Antigravity or any generated adapter.
- Keep Alfa's source of truth in root repo files; `.agent/` is a derived view.
- Treat `user-context/` as the in-kit context repo only because `user-context/.jm-adk-context.json` declares `jm-adk-user-context`; private contents remain ignored by default.

## Placement & Naming Contract

Task deliverables → `workspace/{active}/artifacts/` (never mixed with system files); kit internals → maintainer mode only; filenames + slugs = kebab-case, concise, mnemonic. No hooks here → apply manually. Full contract: `references/ontology/placement-naming-contract.md`.

## Validation

```bash
bash scripts/adapters/antigravity.sh
python3 scripts/check-devkit-readiness.py
```
