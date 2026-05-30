#!/bin/bash
# artifact-placement-guard.sh — PreToolUse placement enforcement (v1.0.0)
#
# WHY: The "every artifact goes to workspace/{active}/artifacts/" rule lived only
# in CLAUDE.md/PRISTINO.md prose. Prose decays as the kit grows and sessions run
# long; hooks do not. This guard moves placement from advisory to deterministic.
#
# CONTRACT:
#   Exit 2 = block the write (forces correct location). Exit 0 = allow.
#   Classifies by DESTINATION, never by prompt intent (paths are facts; prompts lie).
#   Three buckets:
#     1. workspace/{active}/...   → ALLOW  (correct task artifact)
#     2. kit system paths         → ALLOW only in maintainer mode, else BLOCK+route
#     3. ad-hoc anywhere else     → BLOCK + route to active workspace (create if none)
#
# Policy is hot-reloaded from references/guardrails/placement-policy.json on every
# call. If python3 or the policy file is unavailable, the guard fails OPEN (exit 0)
# so a broken guard never bricks the session.
set -uo pipefail

TOOL="${CLAUDE_TOOL_NAME:-}"
INPUT="${CLAUDE_TOOL_INPUT:-}"

# Only police write tools. Everything else passes untouched.
case "$TOOL" in
  Write|Edit|MultiEdit|NotebookEdit) ;;
  *) exit 0 ;;
esac

ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel 2>/dev/null)" || exit 0
POLICY="$ROOT/references/guardrails/placement-policy.json"
[ -f "$POLICY" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

# Maintainer mode: kit-internal edits are legitimate work, not ad-hoc drops.
MODE="task"
[ "${JM_ADK_MODE:-}" = "maintainer" ] && MODE="maintainer"
[ -f "$ROOT/.maintainer" ] && MODE="maintainer"

DECISION="$(
  CLAUDE_TOOL_INPUT="$INPUT" ROOT="$ROOT" POLICY="$POLICY" MODE="$MODE" \
  python3 - <<'PY'
import json, os, re, sys, fnmatch, unicodedata

inp    = os.environ.get("CLAUDE_TOOL_INPUT", "")
root   = os.environ.get("ROOT", "")
mode   = os.environ.get("MODE", "task")
policy = os.environ.get("POLICY", "")

# Extract the target path from the tool-input JSON.
try:
    d = json.loads(inp)
except Exception:
    print("OK"); sys.exit()
target = d.get("file_path") or d.get("notebook_path") or ""
if not target:
    print("OK"); sys.exit()

# Resolve symlinks on both sides (macOS /tmp → /private/tmp, etc.) before compare.
if root:
    root = os.path.realpath(root)
abs_target = os.path.realpath(target) if os.path.isabs(target) else os.path.realpath(os.path.join(root, target))

# Writes outside the project root are out of scope for this guard.
if root and not abs_target.startswith(root + os.sep):
    print("OK"); sys.exit()

# Normalise to a repo-relative path.
rel = abs_target[len(root):].lstrip("/") if root else target
rel = rel.lstrip("./")

try:
    p = json.load(open(policy, encoding="utf-8"))
except Exception:
    print("OK"); sys.exit()

def match(globs):
    # A glob without "/" is a root-level pattern: it must only match a top-level
    # file, never a nested path (Python fnmatch lets "*" span "/", so anchor it).
    for g in globs:
        if "/" in g:
            if fnmatch.fnmatch(rel, g):
                return True
        elif "/" not in rel and fnmatch.fnmatch(rel, g):
            return True
    return False

# ── Naming check (new files only; never break existing names) ──
def suggest(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    if "." in s:
        stem, ext = s.rsplit(".", 1)
        return "%s.%s" % (re.sub(r"[^a-z0-9]+", "-", stem).strip("-") or "archivo", ext)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "archivo"

naming = p.get("naming", {})
if naming.get("enabled") and not os.path.exists(abs_target):
    base = os.path.basename(rel)
    allow = base in set(naming.get("allow_exact", [])) or base.startswith(".") \
        or base.startswith("_TEMPLATE-") or base.endswith(".gitkeep")
    stem = base.rsplit(".", 1)[0] if "." in base else base
    ext_ok = (("." not in base) or re.match(r"^[a-z0-9]+$", base.rsplit(".",1)[1] or ""))
    kebab = bool(re.match(r"^[a-z0-9]+(-[a-z0-9]+)*$", stem)) and ext_ok
    if not (allow or kebab):
        print("DENY:nombre '%s' no es kebab-case. Renombra a '%s' "
              "(minusculas, guiones, sin espacios/acentos)." % (base, suggest(base)))
        sys.exit()

# 1. Correct task artifact location.
if match(p.get("task_artifact_globs", [])):
    print("OK"); sys.exit()

# 2. Kit-internal system path: allowed only when explicitly maintaining the kit.
if match(p.get("system_globs", [])):
    if mode == "maintainer":
        print("OK")
    else:
        print("DENY:ruta de sistema '%s' editable solo en modo maintainer "
              "(export JM_ADK_MODE=maintainer o crea ./.maintainer). "
              "Si es un entregable de tarea, va en workspace/{active}/artifacts/." % rel)
    sys.exit()

# 3. Ad-hoc destination: route to the active workspace.
active = ""
reg = os.path.join(root, "workspace", ".workspace-registry.json")
if os.path.exists(reg):
    try:
        active = json.load(open(reg, encoding="utf-8")).get("activeWorkspace") or ""
    except Exception:
        active = ""

if active and active != "null":
    print("DENY:artefacto ad-hoc '%s' fuera de workspace. "
          "Escribe en workspace/%s/artifacts/ y reintenta." % (rel, active))
else:
    print("DENY:sin workspace activo para '%s'. "
          "Corre: bash scripts/workspace-manager.sh ensure \"<descripcion-tarea>\" "
          "y reintenta la escritura dentro de workspace/{id}/artifacts/." % rel)
PY
)"

case "$DECISION" in
  DENY:*)
    echo "BLOCKED (placement): ${DECISION#DENY:}" >&2
    exit 2
    ;;
  *)
    exit 0
    ;;
esac
