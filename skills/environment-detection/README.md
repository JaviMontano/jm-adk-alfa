# Environment Detection

Detect the active AI coding environment from local, reproducible signals: instruction files, tool availability, repository markers, and explicitly supplied model/context data. The skill then maps those signals to a capability profile, triad mode, model tier, context budget, and bootstrap loading plan.

Use this skill at session start or when the user asks to configure runtime behavior for Codex, Claude Code, Cursor, Windsurf, Gemini, Antigravity, Copilot, or an unknown assistant host.

## Deterministic Contract

- Prefer local evidence over assumptions: files, available tools, command outputs, and user-supplied model metadata.
- Do not call the network, current time, random sources, browser history, cookies, or external account state to identify the environment.
- If signals conflict, emit a `warn` report with the conflict listed instead of forcing a confident result.
- If model context capacity is unknown, choose conservative loading and avoid L3/full-history recommendations.
- Validate machine-readable reports with `scripts/check.sh`.

## Output

The expected deliverable is an environment detection report with:

- `environment`: IDE, model, tier, triad mode, context budget, confidence.
- `signals`: evidence-tagged observations used for detection.
- `capabilities`: local tool and orchestration capabilities.
- `decisions`: traceable mapping from signals to mode, tier, and loading plan.
- `loading_plan`: bounded L1/L2/L3/SKIP resource choices.
- `validation`: pass/warn/block status and checks run.

See `assets/environment-report-contract.json` and `examples/example-output.md` for the concrete shape.
