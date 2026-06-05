# Workflow Forge Scripts

## compile-workflow-forge.py

Offline compiler for slash-command workflow definitions. It reads a structured
JSON workflow spec, validates it against local assets, and renders deterministic
Markdown or JSON.

The script never calls external APIs, MCP tools, network resources, or model
providers.

## check.sh

Runs the positive workflow fixture, validates expected Markdown and JSON output,
and verifies negative fixtures fail closed for single-phase workflows, missing
final verification, and prohibited stack references.
