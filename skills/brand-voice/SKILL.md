---
name: brand-voice
description: 
  This skill should be used when the user asks to "apply brand voice",
  "write in our brand tone", "review copy for brand consistency",
  "create brand writing guidelines", or "calibrate tone for a proposal",
  or mentions voice pillars, tone calibration, or vocabulary mapping. [EXPLICIT]
  It applies configurable brand voice and tone guidelines by reading brand config
  to adapt voice pillars, content type calibration, vocabulary mapping, and writing rules. [EXPLICIT]
  Use this skill whenever the user needs branded written content or voice
  consistency checks, even if they don't explicitly ask for "brand voice". [EXPLICIT]
argument-hint: "content-type text-or-path [brand-config-path]"
model: opus
context: fork
allowed-tools:
  - Read
  - Grep
  - Glob
  - Write
  - Edit
version: 1.0.0
---

# Brand Voice & Tone

Apply configurable brand voice to any written content. Reads brand identity from a config file and adapts voice pillars, vocabulary, tone calibration, and writing patterns accordingly. [EXPLICIT]

## Brand Configuration

Search for brand voice config in this order:
1. Path passed as argument
2. `./brand-voice.json` in working directory
3. `./brand-config.json` (voice section)
4. `~/.claude/brand-voice.json`

### Config Schema

```json
{
  "brand": {
    "name": "YourBrand",
    "positioning": "Your positioning statement",
    "claim": "Your main tagline or claim",
    "claimVariants": [
      "Variant 1. Tagline.",
      "Variant 2. Tagline."
    ],
    "philosophy": "Core philosophy or methodology"
  },
  "voice": {
    "pillars": [
      {
        "name": "Pillar Name",
        "description": "What this pillar means",
        "guidelines": ["Guideline 1", "Guideline 2"]
      }
    ]
  },
  "vocabulary": {
    "preferred": {
      "generic term": "brand term",
      "deliverables": "results"
    },
    "avoid": ["synergy", "leverage", "seamless"]
  },
  "toneCalibration": {
    "proposals": "confident + structured",
    "marketing": "warm + energetic",
    "technical": "clear + precise",
    "internal": "friendly + direct",
    "crisis": "calm + accountable"
  },
  "closingLines": {
    "external": ["Closing line 1", "Closing line 2"],
    "proposals": ["Proposal closing 1"],
    "internal": ["Internal closing 1"]
  }
}
```

### Default (No Config)

If no config found, use professional neutral voice: clear, direct, active voice, no jargon, human-centered. Prompt user to provide brand config for branded output. [EXPLICIT]

## Voice Pillars

Read from `voice.pillars` in config. Default 4-pillar framework:

### 1. Close & Human
Companion, not vendor. Warm, direct, personal. Talk TO people, not AT them. Use "we" and "you" naturally. [EXPLICIT]

### 2. Confident & Grounded
Lead with facts, not adjectives. Active voice. Confidence without arrogance: "We deliver" not "We are proud to deliver."

### 3. Forward-Looking & Optimistic
Focus on progress, not perfection. Frame challenges as opportunities. End on a forward note. [EXPLICIT]

### 4. Simple & Direct
Short sentences. One idea per sentence. Avoid jargon when plain language works. Active verbs: build, deliver, transform, improve. [EXPLICIT]

## Writing by Content Type

### Headlines & Titles
Short, punchy, sentence case. Lead with action or aspiration. Optionally highlight one key word in brand primary color. [EXPLICIT]

### Body Copy
2-4 sentences per block. Active voice. End with forward-looking statement or CTA. Subtly reference brand philosophy. [EXPLICIT]

### Proposals & Reports
Open with client's challenge, not credentials. Data-anchor claims. Structure: Context > Approach > Expected Impact. Close with warm, direct invitation. [EXPLICIT]

### Social / LinkedIn
Start with human hook. Conversational, no buzzwords. Concrete insight or takeaway. End with tagline when appropriate. [EXPLICIT]

### Emails (External)
Clear subject (benefit or question). Reference specific context. One key message. Single CTA. Warm professional sign-off. [EXPLICIT]

### Slide Text
6-10 words max per headline. No full paragraphs. "Eyebrow + headline" structure. Tagline on closing slides. [EXPLICIT]

### Internal Communications
Same warmth, slightly more informal. Reference team identity. Celebrate small wins, frame feedback as improvement. [EXPLICIT]

## Language Rules

**Do use:** We, our, you, your. Build, deliver, transform, improve, create, evolve. Sentence case for headlines.

**Avoid:** Synergy, leverage, seamless, cutting-edge, world-class, innovative (unless earned). Passive voice. Exclamation marks in professional contexts. ALL CAPS. Vague superlatives without proof.

Read additional rules from `vocabulary.preferred` and `vocabulary.avoid` in config. [EXPLICIT]

## Tone Calibration

Read from `toneCalibration` in config. Default matrix:

| Context | Tone | Notes |
|---------|------|-------|
| Corporate proposals | Confident + structured | Facts-forward, evidence-based |
| Marketing / social | Warm + energetic | Human stories, optimism |
| Recruiting / talent | Inspiring + honest | Growth mindset |
| Technical docs | Clear + precise | Plain language |
| Events / launches | Bold + celebratory | Claims front and center |
| Internal | Friendly + direct | Informal, motivating |
| Crisis / issues | Calm + accountable | Transparent, solution-focused |

## Claim & Tagline System

Read from `brand.claim` and `brand.claimVariants`. [EXPLICIT]

**Rules:**
- Claims work as standalone statements
- Extended variants follow the pattern: "[Adjective] [noun]. [Separator]."
- Positioning tag works as sign-off or label

## Manifesto Tone Pattern

For high-impact copy, use anaphoric structure from brand philosophy:
```
Every [moment/person/project/step] [is/has/connects]. [EXPLICIT]
That's why we [action]. [EXPLICIT]
```

## Assumptions & Limits

- Voice config is optional; skill works with defaults but output is generic
- Cannot invent brand identity — needs config or user-provided brand context
- Tone calibration is a dial, not a switch — content types blend tones
- Vocabulary mapping covers common substitutions; domain-specific terms need explicit config
- Not a copywriting skill — provides voice guidelines; actual copy requires creative judgment

## Edge Cases

- **No brand config:** Use neutral professional defaults; note output is unbranded
- **Conflicting tone context (crisis + marketing):** Crisis tone always wins in blended contexts
- **Non-English content:** Apply same voice pillars; adapt vocabulary to target language idioms
- **Multiple brands:** Accept brand config path as argument; switch per invocation

## Validation Gate

- [ ] Brand config loaded (or defaults applied with note)
- [ ] Voice pillars applied consistently throughout content
- [ ] Vocabulary uses preferred terms, avoids banned terms
- [ ] Tone matches content type calibration
- [ ] Active voice dominant (< 15% passive)
- [ ] Headlines in sentence case
- [ ] Closing line appropriate to context
- [ ] No jargon without explanation

---
**Author:** Javier Montano | **Last updated:** March 18, 2026

## Usage

Example invocations:

- "/brand-voice" — Run the full brand voice workflow
- "brand voice on this project" — Apply to current context

