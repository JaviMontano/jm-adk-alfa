---
name: google-sheets-mcp
author: JM Labs (Javier Montano)
version: 1.0.0
description: >
  Google Sheets integration via MCP for deterministic spreadsheet read/write
  plans, least-privilege scopes, and human-confirmed mutations. [DOC]
  Trigger: "spreadsheet", "google sheets", "sheet data", "cells", "ranges",
  "values.get", "values.update", "values.append", "batchUpdate"
status: production
tags: [mcp, google-sheets, spreadsheets, data, automation, google]
mcp-server: workspace-mcp
allowed-tools:
  - Read
  - Write
  - Bash
  - mcp__workspace-mcp__read_sheet_values
  - mcp__workspace-mcp__modify_sheet_values
  - mcp__workspace-mcp__create_spreadsheet
  - mcp__workspace-mcp__list_spreadsheets
  - mcp__workspace-mcp__get_spreadsheet_info
  - mcp__workspace-mcp__format_sheet_range
---

# Google Sheets MCP

> Data workflows are safest when read discovery, scope review, and mutation
> confirmation are explicit. [INFERENCE]

## TL;DR

Use this skill to compile or execute a Google Sheets MCP plan that is grounded
in the official Sheets REST API and local `workspace-mcp` setup docs. [DOC]
The deterministic offline compiler is `scripts/compile-google-sheets-mcp.py`;
it reads `assets/` plus JSON fixtures and never calls Google, OAuth, network, or
MCP tools. [CODE]

## Prerequisites

- Google Workspace MCP server configured from `docs/google-workspace-mcp-setup.md`. [DOC]
- Project MCP conventions aligned with `docs/mcp-integration.md`. [DOC]
- Google Sheets API enabled and OAuth scopes selected with least privilege. [DOC]
- Human confirmation captured before any create/update/append/format mutation. [CODE]

## Deterministic Assets

- `assets/google-sheets-mcp-schema.json` defines the stable input schema. [CODE]
- `assets/scope-policy.json` encodes minimum Sheets/Drive scopes and the official scope-binding note. [DOC]
- `assets/mcp-tool-contract.json` maps local `workspace-mcp` tool names to official Sheets REST operations. [CODE]
- `assets/operation-safety-policy.json` defines read-only-first and confirmation gates. [CODE]
- `assets/value-range-policy.json` captures ValueRange and value method defaults. [DOC]
- `assets/batch-update-policy.json` captures structural `spreadsheets.batchUpdate` rules. [DOC]
- `assets/google-sheets-mcp-template.md` renders the offline report. [CODE]

## Procedure

### Step 1: Classify Intent

- Read-only intents use `spreadsheets.get` or `spreadsheets.values.get`. [DOC]
- Mutating intents use `spreadsheets.create`, `spreadsheets.batchUpdate`, `spreadsheets.values.update`, `spreadsheets.values.append`, or `spreadsheets.values.batchUpdate`. [DOC]
- Mixed intents must begin with read-only discovery. [CODE]

### Step 2: Select Minimum Scope

- Use `https://www.googleapis.com/auth/spreadsheets.readonly` for read-only Sheets metadata and values. [DOC]
- Use `https://www.googleapis.com/auth/drive.file` for app-created or app-opened spreadsheet mutations when that per-file model is sufficient. [DOC]
- Escalate to `https://www.googleapis.com/auth/spreadsheets` only when the workflow must edit accessible Sheets beyond the app-created/opened file boundary. [INFERENCE]
- Do not model scopes at sheet/tab granularity: official Sheets scopes apply to the spreadsheet file and cannot be limited to an individual sheet. [DOC]

### Step 3: Build Operation Plan

- Use `spreadsheets.get` with field masks/ranges before writing to a known spreadsheet. [DOC]
- Use `spreadsheets.create` for new spreadsheet resources. [DOC]
- Use `spreadsheets.batchUpdate` for structural changes such as sheets, formatting, protected ranges, dimensions, and data validation. [DOC]
- Use `spreadsheets.values.get/update/append/batchUpdate` for cell value workflows. [DOC]

### Step 4: Gate Mutations

- Every mutating operation requires `human_confirmation.status=confirmed`. [CODE]
- Mutating workflows must start with a read-only operation unless the user explicitly revises the JSON contract and review accepts that exception. [CODE]
- The local compiler emits a plan/checklist only; live MCP execution remains a separate human-reviewed step. [CODE]

## Quality Criteria

- [ ] Operation names map to official Sheets REST methods. [DOC]
- [ ] Scope profile is the minimum viable profile for each operation. [DOC]
- [ ] Scope binding is `spreadsheet_file`, never `sheet_tab`. [DOC]
- [ ] Mutations have human confirmation and read-only-first discovery. [CODE]
- [ ] Value writes specify `valueInputOption` and a valid `ValueRange`. [DOC]
- [ ] Structural updates use `spreadsheets.batchUpdate` and acknowledge atomic request behavior. [DOC]
- [ ] Output uses evidence tags and records residual risks. [CODE]
- [ ] `bash skills/google-sheets-mcp/scripts/check.sh` passes offline. [CODE]

## Anti-Patterns

- Requesting `drive` or `drive.readonly` by default for Sheets-only work. [DOC]
- Claiming OAuth scopes can be limited to a single sheet/tab. [DOC]
- Running value updates without a prior `spreadsheets.get` or `values.get` review. [CODE]
- Writing formulas or ranges without checking formula impact and protected ranges. [INFERENCE]
- Using individual updates when `spreadsheets.values.batchUpdate` is a clearer bulk write plan. [INFERENCE]

## Related Skills

- `google-drive-mcp` for file search, permissions, upload/export, and per-file access context. [DOC]
- `google-docs-mcp` and `google-slides-mcp` for adjacent Workspace deliverables. [DOC]
- `data-analysis` for analysis after Sheets data has been read safely. [INFERENCE]

## Usage

- `/google-sheets-mcp` to plan spreadsheet reads or mutations. [CODE]
- `python3 skills/google-sheets-mcp/scripts/compile-google-sheets-mcp.py --input skills/google-sheets-mcp/scripts/fixtures/google-sheets-mcp-input.json`. [CODE]
- `bash skills/google-sheets-mcp/scripts/check.sh`. [CODE]

## Assumptions & Limits

- The compiler is offline and does not verify live spreadsheet IDs, OAuth tokens, permissions, formulas, or collaborator state. [CODE]
- Live execution must use the configured `workspace-mcp` server and its currently exposed tool names. [CONFIG]
- A1 notation is required for values operations in this skill contract. [CODE]
- Google notes collaborative spreadsheets can alter final state relative to concurrent collaborator changes after `batchUpdate`. [DOC]
