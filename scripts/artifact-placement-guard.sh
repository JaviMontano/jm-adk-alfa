#!/bin/bash
# artifact-placement-guard.sh — PreToolUse placement + naming enforcement (v2.0.0)
#
# WHY: The "every artifact goes to workspace/{active}/artifacts/" rule + the
# kebab-case naming standard lived only in prose. Prose decays as the kit grows
# and sessions run long; hooks do not. This guard makes both deterministic.
#
# CONTRACT:
#   Reads the tool payload from STDIN (Claude Code: {"tool_name","tool_input"})
#   AND/OR env vars (jm-adk custom runtime: $CLAUDE_TOOL_NAME/$CLAUDE_TOOL_INPUT).
#   Dual-input so it fires under either runtime.
#   Exit 2 + stderr = block (forces correct location/name). Exit 0 = allow.
#   Classifies by DESTINATION, never by prompt intent (paths are facts).
#     1. workspace/{active}/...   → ALLOW  (task artifact)
#     2. kit system paths         → ALLOW only in maintainer mode, else BLOCK+route
#     3. ad-hoc anywhere else     → BLOCK + route to active workspace
#   Naming: every NEW path segment must be kebab (file) / space+caps-free (dir).
#   Fails OPEN (exit 0) if python3/policy missing — a broken guard never bricks
#   the session.
set -uo pipefail

PAYLOAD="$(cat 2>/dev/null)"
ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel 2>/dev/null)" || exit 0
POLICY="$ROOT/references/guardrails/placement-policy.json"
[ -f "$POLICY" ] || exit 0
command -v python3 >/dev/null 2>&1 || exit 0

MODE="task"
[ "${JM_ADK_MODE:-}" = "maintainer" ] && MODE="maintainer"
[ -f "$ROOT/.maintainer" ] && MODE="maintainer"

DECISION="$(
  PAYLOAD="$PAYLOAD" ROOT="$ROOT" POLICY="$POLICY" MODE="$MODE" \
  CLAUDE_TOOL_NAME="${CLAUDE_TOOL_NAME:-}" CLAUDE_TOOL_INPUT="${CLAUDE_TOOL_INPUT:-}" \
  python3 - <<'PY'
import json, os, re, sys, fnmatch, unicodedata

payload = os.environ.get("PAYLOAD", "")
root    = os.environ.get("ROOT", "")
mode    = os.environ.get("MODE", "task")
policy  = os.environ.get("POLICY", "")

# ── Resolve tool + input from stdin (Claude Code) or env (jm-adk runtime) ──
obj = None
if payload:
    try: obj = json.loads(payload)
    except Exception: obj = None
if isinstance(obj, dict) and ("tool_name" in obj or "tool_input" in obj):
    tool = obj.get("tool_name") or os.environ.get("CLAUDE_TOOL_NAME", "")
    ti = obj.get("tool_input") or {}
else:
    tool = os.environ.get("CLAUDE_TOOL_NAME", "")
    raw = os.environ.get("CLAUDE_TOOL_INPUT", "")
    try: ti = json.loads(raw) if raw else {}
    except Exception: ti = {}
if isinstance(ti, str):
    try: ti = json.loads(ti)
    except Exception: ti = {}

if tool not in ("Write", "Edit", "MultiEdit", "NotebookEdit"):
    print("OK"); sys.exit()
target = ti.get("file_path") or ti.get("notebook_path") or ""
if not target:
    print("OK"); sys.exit()

# Resolve symlinks both sides (macOS /tmp → /private/tmp) before compare.
if root:
    root = os.path.realpath(root)
abs_target = os.path.realpath(target) if os.path.isabs(target) else os.path.realpath(os.path.join(root, target))
if root and not abs_target.startswith(root + os.sep):
    print("OK"); sys.exit()           # outside repo → not our business

rel = abs_target[len(root):].lstrip("/") if root else target
if rel.startswith("./"):              # strip a leading "./" PREFIX only — not a
    rel = rel[2:]                     # char set (lstrip("./") would eat ".specify"→"specify")
if not rel:
    print("OK"); sys.exit()

try:
    p = json.load(open(policy, encoding="utf-8"))
except Exception:
    print("OK"); sys.exit()

def match(globs):
    # Root-level glob (no "/") must only match a top-level entry; Python fnmatch
    # lets "*" span "/", so anchor it.
    for g in globs:
        if "/" in g:
            if fnmatch.fnmatch(rel, g): return True
        elif "/" not in rel and fnmatch.fnmatch(rel, g): return True
    return False

# ── Naming: validate every NEW path segment (dirs + leaf file) ──
def slugify_seg(name):
    s = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode().lower()
    if "." in s:
        stem, ext = s.rsplit(".", 1)
        return "%s.%s" % (re.sub(r"[^a-z0-9]+", "-", stem).strip("-") or "x", ext)
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-") or "x"

# Maintainer mode → free (placement + naming). Must precede the naming check:
# governance/generators edit paths with their own conventions.
if mode == "maintainer":
    print("OK"); sys.exit()

naming = p.get("naming", {})
if naming.get("enabled"):
    allow_exact = set(naming.get("allow_exact", []))
    cur = root
    parts = rel.split("/")
    for i, seg in enumerate(parts):
        cur = os.path.join(cur, seg)
        if os.path.exists(cur):
            continue                                   # existing entry — never rename
        is_leaf = (i == len(parts) - 1)
        if seg.startswith(".") or seg.startswith("_") or seg in allow_exact:
            continue                                   # dotfiles, _templates/_tasks, allowlist
        if is_leaf:
            stem = seg.rsplit(".", 1)[0] if "." in seg else seg
            ext_ok = ("." not in seg) or bool(re.match(r"^[a-z0-9]+$", seg.rsplit(".", 1)[1] or ""))
            # Snake-allowed zones (e.g. dated ADR/log files YYYYMMDD_scope_slug).
            snake = match(naming.get("snake_allowed_globs", []))
            pat = r"^[a-z0-9]+([_-][a-z0-9]+)*$" if snake else r"^[a-z0-9]+(-[a-z0-9]+)*$"
            if re.match(pat, stem) and ext_ok:
                continue
            kind = "kebab/snake" if snake else "kebab-case"
            print("DENY:nombre '%s' no es %s. Renombra a '%s' "
                  "(minusculas, guiones, sin espacios/acentos)." % (seg, kind, slugify_seg(seg))); sys.exit()
        else:
            # Dir: permissive — allow kebab, snake, T-NNN, acronyms. Block only the
            # unambiguous ad-hoc signals: spaces or non-ASCII (accents, symbols).
            if " " not in seg and not re.search(r"[^A-Za-z0-9._-]", seg):
                continue
            print("DENY:carpeta nueva '%s' invalida (sin espacios ni acentos). "
                  "Usa '%s'." % (seg, slugify_seg(seg))); sys.exit()

# 1. Correct task artifact location.
if match(p.get("task_artifact_globs", [])):
    print("OK"); sys.exit()

# 2. In-kit user context repo: allowed only for explicit context updates.
if match(p.get("context_repo_globs", [])):
    env_name = p.get("context_repo_write_env", "JM_ADK_CONTEXT_WRITE")
    if os.environ.get(env_name) == "1":
        print("OK")
    else:
        print("DENY:ruta de contexto '%s' requiere actualizacion explicita. "
              "Si el usuario pidio recordar/actualizar contexto, reintenta con %s=1. "
              "Los entregables de tarea siguen yendo a workspace/{active}/artifacts/." % (rel, env_name))
    sys.exit()

# 3. Kit-internal system path: allowed only when maintaining the kit.
if match(p.get("system_globs", [])):
    if mode == "maintainer":
        print("OK")
    else:
        print("DENY:ruta de sistema '%s' editable solo en modo maintainer "
              "(export JM_ADK_MODE=maintainer o crea ./.maintainer). "
              "Si es un entregable de tarea, va en workspace/{active}/artifacts/." % rel)
    sys.exit()

# 4. Ad-hoc destination: route to the active workspace.
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
          "y reintenta dentro de workspace/{id}/artifacts/." % rel)
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
