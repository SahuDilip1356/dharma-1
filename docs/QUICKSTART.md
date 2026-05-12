# Dharma 1.0 — Quickstart

60 seconds from clone to first Route Receipt.

## Install

```bash
git clone <dharma-repo>
cd your-project
/path/to/dharma/install.sh
```

What this does:
- Copies the 23-skill catalog to `.dharma/skills/`
- Installs `commit-msg` and `pre-push` git hooks
- Scaffolds `memory/` 3-drawer (STATE, semantic, decisions, learnings, episodic)
- Installs the router script + CLI wrapper at `.dharma/dharma`

## Your first run

```bash
# 1. Classify the task — get a Route Receipt
.dharma/dharma route "add a chatbot that answers patient FAQs"

# Output:
# [Route B — New Feature]
#   Start: /intent
#   Overlays: risk, ai
#   Forced gates: /cso, /codex, /qa, /ai-economics, /ai-safety, /ai-observability
#   Exit evidence needed: PRD contract; Plan complete; Evidence ledger

# 2. List all skills
.dharma/dharma skills

# 3. Read a skill's contract
cat .dharma/skills/p0-intent/intent/SKILL.md
```

## The flow (recommended order)

| Phase | When | Skill(s) | Output |
|---|---|---|---|
| P0 Intent | Every new work cycle | `/intent`, `/route` | PRD contract + Route Receipt |
| P1 Plan | Before code | `/plan-ceo`, `/plan-eng`, `/plan-design` | Scope + architecture + design rating |
| P2 Design | If user-facing | `/design-shotgun`, `/design-build` | Approved variant + production HTML |
| P3 Build | Coding phase | `/karpathy-check`, `/investigate`, `/review` | Code + reviews clean |
| P4 Verify | Before push | `/qa`, `/cso`, `/codex`, `/evidence` | Receipts for each gate |
| P5 Ship | Push + deploy | `/risk-gate`, `/ship`, `/land-and-deploy`, `/canary` | Merged, deployed, monitored |
| P6 Learn | Weekly | `/retro`, `/benchmark` | Patterns promoted to semantic memory |

**AI Overlay** fires automatically (via router) when the task involves LLMs:
- `/ai-economics` in P1 — model selection + cost ceiling
- `/ai-safety` in P3 — adversarial + hallucination + prompt-injection eval
- `/ai-observability` in P5 — telemetry + drift detection

## Try the hooks

```bash
# Evidence ledger blocks banned phrases
git commit -m "fix login: should work now"
# ✗ evidence-ledger: commit message contains banned phrase: "should work"

# Use a valid completion state
git commit -m "fix login: implemented and verified with tests/auth.spec.ts:42"
# ✓ accepted
```

## Risk overlay (pre-push)

Push a diff touching `auth/`, `payments/`, `migrations/`, `prompts/`, or `policy.*`?
The pre-push hook checks for fresh `/cso`, `/codex`, `/qa` receipts in `memory/`.
Missing → push blocked with the list of gates to run.

Bypass (logged to learnings):
```bash
DHARMA_RISK_BYPASS="staging-only, no real users yet" git push
```

## Memory drawers

```
memory/
├── STATE.md           # Working memory — current phase, blockers, next step
├── semantic.md        # Durable patterns, taste, anti-patterns
├── decisions.md       # Append-only log of decisions + rationale
├── learnings.md       # Append-only log of failures + fixes
└── episodic/          # Session digests as YYYY-MM-DD-slug.md
```

The `memory-layer` pattern: every skill reads STATE + semantic before running, and writes back decisions/learnings on exit. `/retro` mines `episodic/` weekly and promotes patterns into `semantic.md`.

## What's next

- M2: AI-native layer goes live (currently stub skills)
- M3: GitHub Pages site, telemetry opt-in, Show HN

For full architecture: `docs/ARCHITECTURE.md` (TBD).
For ethos and design positions: `ETHOS.md`.
For project-level config: `.dharma/config.yaml`.
