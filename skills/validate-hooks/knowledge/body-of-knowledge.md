# Validate Hooks Body Of Knowledge

## Canon

- [DOC] `references/hook-compatibility-matrix.md` defines the human-readable hook compatibility rule.
- [CODE] `assets/hook-compatibility-matrix.json` defines the executable compatibility matrix used by `scripts/compile-validate-hooks.py`.
- [CODE] `assets/hooks-audit-schema.json` defines the structured audit input contract.
- [CODE] `assets/command-safety-policy.json` defines offline command-string safety checks.
- [CODE] `assets/placement-guard-expectations.json` defines the required placement guard shape.

## Hook Runtime Rules

- [CODE] Recognized hook events total 22.
- [CODE] `command` and `http` hooks are compatible with all recognized events.
- [CODE] `prompt` and `agent` hooks require ToolUseContext.
- [CODE] ToolUseContext is available only for `PreToolUse`, `PermissionRequest`, and `PostToolUse`.
- [CODE] `prompt` or `agent` on `SessionStart`, `UserPromptSubmit`, `PostToolUseFailure`, `Stop`, or any other non-ToolUseContext event is a critical finding.
- [CODE] Canonical `hooks.json` shape is an object keyed by event name: `{"hooks": {"PreToolUse": [{"type": "command"}]}}`.
- [CODE] A flat array under `hooks` is reported as a critical structure finding because it is not the canonical event-keyed schema for this skill.

## Offline Audit Responsibilities

| Responsibility | Deterministic Check |
|---|---|
| Structure | Validate `hooks` key and event-keyed object shape. |
| Event names | Check every event against the 22-event matrix and suggest common corrections. |
| Hook types | Require `command`, `http`, `prompt`, or `agent`; reject unknown types. |
| ToolUseContext | Reject `prompt` and `agent` outside ToolUseContext events. |
| Payload fields | Require `command`, `url`, `prompt`, or `agent` according to hook type. |
| Command safety | Scan command strings for destructive, privilege, network-pipe, and secret-read patterns. |
| Script references | Verify referenced local scripts exist and warn when shell scripts are not executable. |
| Placement guard | Expect a `PreToolUse` command hook that references `artifact-placement-guard.sh` or `placement-guard`. |

## Non-Execution Boundary

- [CODE] The compiler reads JSON and filesystem metadata only.
- [CODE] The compiler never runs hook commands.
- [CODE] The compiler writes only the report path supplied through `--output`.
- [INFERENCE] Offline analysis cannot prove whether a command will succeed at runtime.

## Quality Metrics

| Metric | Target | How To Measure |
|---|---|---|
| Matrix coverage | 22 events and 4 types | `assets/hook-compatibility-matrix.json` consumed by script. |
| Critical incompatibility detection | 100% for prompt/agent on non-ToolUseContext events | Negative fixture in `scripts/fixtures/invalid-tooluse-context.json`. |
| Structure detection | event-keyed pass, flat-array fail | Positive and flat-array fixtures in `scripts/fixtures/`. |
| Command safety | Pattern-backed findings | `assets/command-safety-policy.json` and deterministic fixture checks. |
| Placement guard | Expected PreToolUse command hook | `assets/placement-guard-expectations.json` and expected fragments. |
