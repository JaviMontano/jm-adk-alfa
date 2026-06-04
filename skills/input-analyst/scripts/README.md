# Input Analyst Scripts

## compile-input-analysis.py

Offline compiler for raw user input analysis. It reads local JSON assets and a
JSON input fixture, then emits a deterministic Markdown or JSON report with:
surface errors, 5 Whys, 7 So-Whats, intent gaps, ambiguity register,
actionability score, clarified prompt, routing hints, privacy flags, and
confidence.

The script never calls external APIs, MCP tools, network resources, or model
providers.

## check.sh

Runs the positive fixture, validates expected Markdown fragments, validates JSON
output shape, and verifies negative fixtures fail for empty input and non-offline
routing.
