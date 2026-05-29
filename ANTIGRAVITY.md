# ANTIGRAVITY.md

## Purpose

Alfa exposes an Antigravity-compatible derived view through `.agent/` and `scripts/adapters/antigravity.sh`. Runtime capability claims remain validation pending until tested in the target Antigravity environment.

## First Use

1. Confirm this repo is Alfa before edits.
2. Run `python3 scripts/diagnose-first-use.py --dry-run`.
3. Use `/jm-adk:first-use` for greeting-only or empty input.
4. Use `/jm-adk:start-task` for explicit tasks.
5. Fall back to Markdown-first instructions when runtime support is unclear.

## Generated View

- `.agent/skills_index.json` indexes root skills.
- `.agent/rules/GEMINI.md` contains generated Antigravity-facing rules.
- `.agent/ARCHITECTURE.md` mirrors current architecture counts where supported.

## Boundaries

- Do not assume hooks, MCP, workspace management, function calling, or multimodal support unless validated in the runtime.
- Do not route secrets through Antigravity or any generated adapter.
- Keep Alfa's source of truth in root repo files; `.agent/` is a derived view.

## Validation

```bash
bash scripts/adapters/antigravity.sh
python3 scripts/check-devkit-readiness.py
```
