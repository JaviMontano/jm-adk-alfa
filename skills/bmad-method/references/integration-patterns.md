# BMAD Integration Patterns — External Tools & Workflows

## Table of Contents
- [Integration Philosophy](#integration-philosophy)
- [Git Hooks](#git-hooks)
- [CI/CD Pipeline Integration](#cicd-pipeline-integration)
- [IDE Integration](#ide-integration)
- [Project Management Tool Sync](#project-management-tool-sync)
- [Communication Tool Integration](#communication-tool-integration)
- [Automation Recipes](#automation-recipes)
- [Custom Validation in CI](#custom-validation-in-ci)

---

## Integration Philosophy

BMAD integrates with external tools by treating Git artifacts as the source of truth and external systems as mirrors or triggers. Data flows outward from BMAD artifacts — never the reverse. Jira tickets reference BMAD stories; BMAD stories never reference Jira tickets as their source.

**Core rule**: BMAD artifacts in Git are authoritative. External tool state (Jira status, Slack messages, dashboard metrics) is derived, never canonical.

**Integration tiers**:
| Tier | Effort | Value | Examples |
|------|--------|-------|---------|
| 1 — Passive | <1 hour | Artifact validation on commit | Pre-commit hooks, linting |
| 2 — Reactive | 1-4 hours | CI gates, automated checks | Pipeline validation, PR templates |
| 3 — Active | 4-16 hours | Bidirectional sync, dashboards | Jira sync, Slack notifications, metrics |

Start at Tier 1. Move up only when the lower tier is stable and the team needs more automation.

---

## Git Hooks

### Pre-Commit: Artifact Schema Validation

Validates BMAD artifact schemas before allowing a commit. Prevents malformed stories, broken frontmatter, and missing required fields.

```bash
#!/usr/bin/env bash
# .git/hooks/pre-commit — BMAD artifact validation
set -euo pipefail

CHANGED_STORIES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^stories/.*\.md$' || true)
CHANGED_EPICS=$(git diff --cached --name-only --diff-filter=ACM | grep -E '^epics/.*\.md$' || true)
CHANGED_SPRINT=$(git diff --cached --name-only --diff-filter=ACM | grep -E 'sprint-status\.ya?ml$' || true)

EXIT_CODE=0

for file in $CHANGED_STORIES; do
  # Validate story frontmatter has required fields
  if ! grep -q '^story-id:' "$file"; then
    echo "ERROR: $file missing story-id in frontmatter"
    EXIT_CODE=1
  fi
  if ! grep -q '^fr-refs:' "$file"; then
    echo "ERROR: $file missing fr-refs (traceability broken)"
    EXIT_CODE=1
  fi
  # Validate points are Fibonacci {1,2,3,5,8}
  POINTS=$(grep '^points:' "$file" | head -1 | awk '{print $2}')
  if [[ -n "$POINTS" ]] && ! echo "1 2 3 5 8" | grep -qw "$POINTS"; then
    echo "ERROR: $file has invalid points value: $POINTS (must be 1,2,3,5,8)"
    EXIT_CODE=1
  fi
done

for file in $CHANGED_EPICS; do
  if ! grep -q '^epic-id:' "$file"; then
    echo "ERROR: $file missing epic-id in frontmatter"
    EXIT_CODE=1
  fi
done

exit $EXIT_CODE
```

### Commit-Message: Story ID Enforcement

Ensures every commit on a feature branch references a BMAD story ID or rapid spec.

```bash
#!/usr/bin/env bash
# .git/hooks/commit-msg — BMAD story ID enforcement
COMMIT_MSG_FILE="$1"
COMMIT_MSG=$(cat "$COMMIT_MSG_FILE")

BRANCH=$(git rev-parse --abbrev-ref HEAD)

# Skip enforcement on main/develop/release branches
if [[ "$BRANCH" =~ ^(main|develop|release) ]]; then
  exit 0
fi

# Require STORY-XXX-NNN or "Rapid Spec:" prefix
if ! echo "$COMMIT_MSG" | grep -qE '(STORY-[A-Z]+-[0-9]{3}|Rapid Spec:)'; then
  echo "ERROR: Commit message must reference a STORY-ID (e.g., STORY-AUTH-001)"
  echo "       or begin with 'Rapid Spec:' for Quick Flow changes."
  echo "       Got: $COMMIT_MSG"
  exit 1
fi
```

### Pre-Push: Gate Check

Blocks pushes to protected branches if the implementation readiness gate has not passed.

```bash
#!/usr/bin/env bash
# .git/hooks/pre-push — BMAD gate validation
REMOTE="$1"

while read local_ref local_sha remote_ref remote_sha; do
  # Only check pushes to develop or main
  if [[ "$remote_ref" =~ refs/heads/(develop|main) ]]; then
    GATE_FILE=$(find . -name "gate-result.*" -path "*/docs/*" 2>/dev/null | head -1)
    if [[ -z "$GATE_FILE" ]]; then
      echo "ERROR: No gate-result file found. Run the implementation readiness gate before pushing to $remote_ref."
      exit 1
    fi
    GATE_RESULT=$(grep -o '"result":\s*"[^"]*"' "$GATE_FILE" 2>/dev/null | head -1 | grep -oE '(PASS|CONCERNS|FAIL)')
    if [[ "$GATE_RESULT" == "FAIL" ]]; then
      echo "ERROR: Implementation readiness gate status is FAIL. Resolve all failures before pushing."
      exit 1
    fi
  fi
done

exit 0
```

---

## CI/CD Pipeline Integration

### GitHub Actions: BMAD Artifact Validation

```yaml
# .github/workflows/bmad-validate.yml
name: BMAD Artifact Validation
on:
  pull_request:
    paths:
      - 'stories/**'
      - 'epics/**'
      - 'planning_artifacts/**'
      - 'architecture/**'
      - 'sprint-status.yaml'

jobs:
  validate-artifacts:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: pip install pyyaml jsonschema

      - name: Validate story schemas
        run: test -f scripts/validate_project.py && python scripts/validate_project.py --stories

      - name: Validate artifact flow
        run: test -f scripts/check_artifact_flow.py && python scripts/check_artifact_flow.py

      - name: Check for orphan stories
        run: |
          test -f scripts/check_artifact_flow.py
          python scripts/check_artifact_flow.py --orphans
          if [ $? -ne 0 ]; then
            echo "::error::Orphan stories detected. Run check_artifact_flow.py locally for details."
            exit 1
          fi
```

### GitHub Actions: Gate as CI Stage

Create a workflow triggered on PRs to `develop`/`main` with path filters for `stories/**` and `architecture/**`. Three steps: (1) Verify `docs/gate-result.json` exists (fail if missing), (2) Parse the JSON and check `result` field is not "FAIL", (3) Print a summary of all 13 steps with pass/warn/fail indicators. Use `python -c` with `json.load()` for parsing. Report gate summary with `if: always()` so it prints even on failure.

### Automated Sprint Status Updates

Create a GitHub Actions workflow triggered on push to `develop`. Extract story IDs from merge commit messages since the last `sprint-status.yaml` update using `git log`. If `scripts/generate_sprint_status.py` exists in the target project, pass the list to it with `--mark-complete`; otherwise write an explicit manual sprint-status update step. Requires `fetch-depth: 0` in the checkout step for full Git history access.

---

## IDE Integration

### VS Code / Cursor

**Workspace settings** (`.vscode/settings.json`):
```json
{
  "files.associations": {
    "*.agent.yaml": "yaml",
    "sprint-status.yaml": "yaml"
  },
  "yaml.schemas": {
    "./schemas/story-schema.json": "stories/*.md",
    "./schemas/epic-schema.json": "epics/*.md"
  },
  "editor.rulers": [100],
  "files.exclude": {
    "**/.bmad/cache": true
  }
}
```

**Recommended extensions**:
- YAML Language Support — schema validation for BMAD YAML artifacts
- Markdown All in One — TOC generation for BMAD reference docs
- GitLens — trace artifact changes through Git history

**Snippets** (`.vscode/bmad.code-snippets`): Create two snippets:
- `bmad-story` (prefix) — Generates full story frontmatter (story-id, epic-ref, title, status, points with choice picker {1,2,3,5,8}, priority picker, fr-refs) plus AC template with Given/When/Then templates
- `bmad-rapid` (prefix) — Generates the rapid spec template (Request, Rationale, Scope, Approach, Acceptance, Risk picker {Low,Medium}, Traceability)

### Claude Code Integration

BMAD works natively with Claude Code through the skill system. Key patterns:

1. **Agent activation**: Load the agent's compiled `.agent.md` as a system prompt
2. **Context loading**: Use the progressive context table — load project-context.md first, then phase-specific artifacts
3. **Workflow execution**: Follow the sharded step files sequentially. Respect HALT directives.
4. **Artifact output**: Write outputs to the paths specified in the workflow step's `outputs` field

**Claude Code session protocol**:
```
1. Start session → Load project-context.md
2. Identify phase → Load phase-specific artifacts per progressive-context.md
3. Activate agent → Load agent persona
4. Execute workflow → Follow step files
5. Validate output → Run validation scripts
6. Commit → Include story ID in commit message
```

---

## Project Management Tool Sync

### Jira / Linear Integration

**Mapping rules**:
| BMAD Artifact | External Tool Equivalent | Sync Direction |
|---------------|------------------------|----------------|
| Epic (EPIC-AUTH) | Jira Epic | BMAD → Jira (create only) |
| Story (STORY-AUTH-001) | Jira Story/Task | BMAD → Jira (create + status sync) |
| Story status | Jira status | Bidirectional (status only) |
| Acceptance criteria | Jira description | BMAD → Jira (link to Git file) |
| Sprint assignment | Jira sprint | BMAD → Jira |
| Story points | Jira story points | BMAD → Jira |

**Implementation approach**: Use a shell script with jira-cli (`github.com/ankitpokhrel/jira-cli`) that iterates over `stories/*.md`, extracts `story-id`, `title`, `points`, and `status` from frontmatter, checks if a matching Jira ticket exists (search by summary containing the story ID), and creates one if not. Run at sprint boundaries. Ticket summary format: `STORY-AUTH-001: Story Title`. Include story points as a custom field and link back to the Git source file in the ticket body.

### GitHub Issues Integration

Use `actions/github-script@v7` to sync stories to GitHub Issues. The workflow triggers on pushes to `stories/*.md` on the develop branch. For each story file, parse `story-id` and `title` from frontmatter. Check if an issue with label `bmad-story` and a matching `[STORY-ID]` prefix exists. If not, create one with the story content as the issue body.

**Key implementation details**:
- Trigger: `push` to `develop` with path filter `stories/*.md`
- Permissions: `issues: write`
- Label all created issues with `bmad-story` for filtering
- Issue title format: `[STORY-AUTH-001] Story Title`
- Issue body: link to source file + full story content

---

## Communication Tool Integration

### Slack Notifications

Post BMAD gate results to Slack using incoming webhooks. Trigger on `workflow_run` completion of the gate validation workflow. Color-code: green for pass, red for fail. Include gate result summary in the attachment text. Store the webhook URL as a repository secret (`SLACK_WEBHOOK_URL`).

---

## Automation Recipes

### Recipe 1: Auto-Generate Traceability Matrix

```bash
#!/usr/bin/env bash
# generate-traceability.sh — Build traceability matrix from artifacts
echo "| FR ID | Epic | Story(ies) | Status |"
echo "|-------|------|------------|--------|"

for story_file in stories/*.md; do
  STORY_ID=$(grep '^story-id:' "$story_file" | awk '{print $2}')
  EPIC_REF=$(grep '^epic-ref:' "$story_file" | awk '{print $2}')
  STATUS=$(grep '^status:' "$story_file" | awk '{print $2}')
  FR_REFS=$(grep -A 20 '^fr-refs:' "$story_file" | grep '^\s*-' | sed 's/^\s*- //' | tr '\n' ', ' | sed 's/, $//')

  for fr in $(echo "$FR_REFS" | tr ',' '\n'); do
    fr=$(echo "$fr" | xargs)
    echo "| $fr | $EPIC_REF | $STORY_ID | $STATUS |"
  done
done | sort
```

### Recipe 2: PR Template with BMAD Checklist

```markdown
<!-- .github/PULL_REQUEST_TEMPLATE.md -->
## BMAD Story Reference
Story ID: STORY-___-___
Epic: EPIC-___

## Changes
<!-- Describe what changed and why -->

## BMAD Checklist
- [ ] All acceptance criteria from the story are met
- [ ] Tests written from Given/When/Then (not from implementation)
- [ ] Code follows project-context.md conventions
- [ ] No files in exclusion zones modified
- [ ] sprint-status.yaml updated
- [ ] Architecture doc updated (if component behavior changed)
```

---

## Custom Validation in CI

### Story-to-FR Traceability Check

```python
#!/usr/bin/env python3
"""Validate that every story traces to at least one FR in the PRD."""
import re, sys, os

def extract_frs_from_prd(prd_path):
    with open(prd_path) as f:
        return set(re.findall(r'FR-[A-Z]+-\d{3}', f.read()))

def extract_frs_from_story(story_path):
    with open(story_path) as f:
        content = f.read()
        refs_section = re.search(r'fr-refs:\s*\n((?:\s+-\s*.+\n)+)', content)
        if refs_section:
            return set(re.findall(r'FR-[A-Z]+-\d{3}', refs_section.group(1)))
    return set()

prd_frs = extract_frs_from_prd('planning_artifacts/PRD.md')
errors = []

for story_file in sorted(os.listdir('stories')):
    if not story_file.endswith('.md'):
        continue
    story_frs = extract_frs_from_story(f'stories/{story_file}')
    if not story_frs:
        errors.append(f'{story_file}: no FR references found')
    for fr in story_frs:
        if fr not in prd_frs:
            errors.append(f'{story_file}: references {fr} which does not exist in PRD')

if errors:
    for e in errors:
        print(f'ERROR: {e}', file=sys.stderr)
    sys.exit(1)
print(f'OK: All stories trace to valid FRs in PRD ({len(prd_frs)} FRs found)')
```

---

## Assumptions

- The team uses Git as version control (hooks and CI examples assume Git)
- CI/CD examples target GitHub Actions; adaptation to GitLab CI, CircleCI, or Jenkins requires syntax changes but identical logic
- External tool APIs (Jira, Slack) require authentication tokens stored as CI secrets

## Limits

- This document provides integration patterns, not production-ready code — scripts must be tested and adapted per project
- Bidirectional sync (e.g., Jira status → BMAD story status) is intentionally simplified; production use requires conflict resolution logic
- IDE snippets cover VS Code/Cursor only — JetBrains, Vim, and Emacs equivalents are not provided

## Acceptance Criteria

- [ ] Git hooks can be installed by running a single setup command
- [ ] CI pipeline validates BMAD artifacts on every PR that touches story or architecture files
- [ ] Story ID enforcement prevents commits without traceability on feature branches
- [ ] At least one IDE snippet exists for story and rapid spec creation

See also: `references/schemas.md`, `references/artifact-flow-chain.md`, `references/phase-4-implementation.md`, `references/brownfield-patterns.md`, `references/enterprise-governance.md`
