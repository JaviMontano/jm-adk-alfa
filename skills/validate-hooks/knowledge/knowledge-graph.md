# Validate Hooks Knowledge Graph

## Core Concepts

- [CODE] `validate-hooks`: offline hook audit skill.
- [CODE] `hooks-json-structure`: canonical event-keyed `hooks` object.
- [CODE] `hook-event`: one of 22 recognized runtime lifecycle events.
- [CODE] `hook-type`: one of `command`, `http`, `prompt`, or `agent`.
- [CODE] `tool-use-context`: runtime context required by `prompt` and `agent`.
- [CODE] `command-safety`: pattern-based inspection of command strings.
- [CODE] `placement-guard`: expected `PreToolUse` command guard for artifact placement.

## Dependencies

- [DOC] Human-readable compatibility source: `references/hook-compatibility-matrix.md`.
- [CODE] Executable compatibility source: `assets/hook-compatibility-matrix.json`.
- [CODE] Compiler: `scripts/compile-validate-hooks.py`.
- [CODE] Fixture gate: `scripts/check.sh`.

## Skill Relationships

- [CODE] Upstream: `plugin-builder`, `build-plugin-scaffold`, and local hook configuration work.
- [CODE] Downstream: `fix-common-issues`, `generate-qa-scorecard`, and `generate-qa-report`.
