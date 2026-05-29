#!/bin/bash
# persona-calibrate.sh v1.0.0 — UserPromptSubmit hook
#
# Deterministic persona auto-calibration + prompt-optimizer signals.
# Reads the user prompt, scores it against references/ontology/personas.json,
# parses mode flags, and emits a model-parseable additionalContext block to stdout.
# Read-only. Always exits 0 (never blocks input). Byte-stable for identical input.
# Security/injection detection stays in user-prompt-filter.sh (single responsibility).

PROMPT="${CLAUDE_USER_PROMPT:-}"
PROJECT_ROOT="$(git -C "$(dirname "$0")/.." rev-parse --show-toplevel 2>/dev/null)" || PROJECT_ROOT="$(dirname "$0")/.."
REGISTRY="$PROJECT_ROOT/references/ontology/personas.json"

# Degrade gracefully if registry or python3 is missing.
if [ ! -f "$REGISTRY" ] || ! command -v python3 >/dev/null 2>&1; then
  echo "PRISTINO-CALIBRATION: DEGRADED (registry or python3 unavailable)"
  exit 0
fi

PROMPT="$PROMPT" REGISTRY="$REGISTRY" python3 - <<'PY'
import json, os, re, sys

prompt = os.environ.get("PROMPT", "")
low = prompt.lower()
try:
    reg = json.load(open(os.environ["REGISTRY"], encoding="utf-8"))
except Exception:
    print("PRISTINO-CALIBRATION: DEGRADED (registry parse error)")
    sys.exit(0)

# ── Mode parse (deterministic regex from registry) ──
modes = reg.get("modes", {})
mode = "full"
if re.search(modes.get("bypass", r"^!"), prompt):
    mode = "bypass"
elif re.search(modes.get("soloPrompt", r"MODO:\s*SOLO_PROMPT"), prompt, re.I):
    mode = "solo_prompt"
elif re.search(modes.get("soloRespuesta", r"MODO:\s*SOLO_RESPUESTA"), prompt, re.I):
    mode = "solo_respuesta"

# ── Score personas (count of trigger substring hits, case-insensitive) ──
personas = reg.get("personas", [])
default = next((p for p in personas if p.get("default")), personas[-1] if personas else None)

def score(p):
    return sum(1 for t in p.get("triggers", []) if t.lower() in low)

scored = [(score(p), p.get("priority", 999), p) for p in personas]
top_score = max((s for s, _, _ in scored), default=0)

if top_score == 0:
    chosen = default
    confidence = 0.50
else:
    # highest score; tie-break by lower priority
    winners = sorted([t for t in scored if t[0] == top_score], key=lambda t: t[1])
    chosen = winners[0][2]
    confidence = min(1.0, 0.5 + 0.25 * top_score)

# ── Complexity heuristic (drives adaptive optimizer) ──
substantive_markers = ("arquitect", "diseñ", "plan", "estrategia", "implementa",
                       "analiza", "compara", "evalúa", "roadmap", "refactor", "optimiza")
substantive = len(prompt) > 80 or any(m in low for m in substantive_markers)
complexity = "substantive" if substantive else "trivial"

delegate = ",".join(chosen.get("capability_agents", [])) if chosen else ""
label = chosen.get("label", "Asesor Experto en la Materia") if chosen else "Asesor Experto en la Materia"
pid = chosen.get("id", "asesor-experto") if chosen else "asesor-experto"
prec = ">".join(reg.get("precedence", ["Veracidad", "Seguridad", "Objetivo", "Formato", "Estilo"]))
threshold = reg.get("confidenceThreshold", 0.6)
low_conf = confidence < threshold

# Optimizer directive per mode + complexity
if mode == "bypass":
    optimizer = "off (plain answer)"
elif mode == "solo_prompt":
    optimizer = "emit section 2 only (optimized prompt)"
elif mode == "solo_respuesta":
    optimizer = "emit section 3 only (response)"
elif complexity == "trivial":
    optimizer = "response only (skip 3-section)"
else:
    optimizer = "3 sections: 1) Pedido original 2) Prompt optimizado 3) Respuesta"

print("PRISTINO-CALIBRATION:")
print(f"PERSONA: {label}")
print(f"PERSONA-ID: {pid}")
print(f"CONFIDENCE: {confidence:.2f}")
print(f"MODE: {mode}")
print(f"COMPLEXITY: {complexity}")
print(f"DELEGATE: {delegate}")
print(f"OPTIMIZER: {optimizer}")
if low_conf and mode != "bypass":
    print(f"LOW-CONFIDENCE: ask <=2 clarifying questions before committing (threshold {threshold})")
print(f"CONTRACT: line1=persona-label; precedence={prec}; evidence-tags=on; declare-confidence=on")
print("IDENTITY: Pristino · MetodologIA · JM Labs")
print("---")
PY

exit 0
