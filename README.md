# Dharma 1.0

> **Build with role. Ship with evidence. Govern with intention.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Status: alpha](https://img.shields.io/badge/status-alpha-orange.svg)](#status--roadmap)
[![Install: 60 seconds](https://img.shields.io/badge/install-60_seconds-brightgreen.svg)](#install)

A unified framework for AI-assisted product development. The synthesis of [**gstack**](https://github.com/garrytan/gstack)'s velocity (roles, real-browser QA, deploy loop) and [**Dharma 0.x**](https://github.com/SahuDilip1356/Dharma)'s discipline (evidence ledger, risk overlay, AI-native governance).

**23 skills. 6 phases. 2 always-on overlays. 60-second install. AI-native by default.**

---

## Table of contents

- [Why Dharma 1.0](#why-dharma-10)
- [Install](#install)
- [Your first run](#your-first-run)
- [The 23 skills](#the-23-skills)
- [Architecture](#architecture)
- [The AI overlay — the strategic moat](#the-ai-overlay--the-strategic-moat)
- [The evidence ledger](#the-evidence-ledger)
- [The deterministic router](#the-deterministic-router)
- [Comparison vs gstack and Dharma 0.x](#comparison-vs-gstack-and-dharma-0x)
- [Repo structure](#repo-structure)
- [Status & roadmap](#status--roadmap)
- [Contributing](#contributing)
- [Lineage & acknowledgments](#lineage--acknowledgments)
- [License](#license)

---

## Why Dharma 1.0

AI coding assistants are fast. They are also undisciplined by default. Without process, the same session that writes clean code will also:

- Skip UX thinking and ship broken empty states
- Miss accessibility entirely on user-facing screens
- Claim "it's done" based on belief, not evidence
- Change auth or migration logic without rollback plan
- Ship LLM-powered features with no token budget, no adversarial test, no observability

These are not model failures. They are process failures.

**gstack** solves velocity. **Dharma 0.x** solves discipline. Dharma 1.0 is the smallest framework that does both:

- **Role gives velocity.** 23 named skills, not generic prompts.
- **Evidence replaces belief.** "Should work" banned at commit time.
- **Risk overlays trump speed.** Diff touches `auth/`, `payments/`, `migrations/`, `prompts/`? Forced security + cross-model review before push.
- **AI features are production systems.** First framework with first-class, executable economics + safety eval + observability.
- **Memory continuity.** Three-drawer model (working / semantic / episodic) survives session boundaries.

---

## Install

```bash
git clone https://github.com/SahuDilip1356/dharma-1.git
cd dharma-1
./install.sh /path/to/your/project
```

What this does (verified <1s in test):
- Copies the 23-skill catalog to `.dharma/skills/`
- Installs `commit-msg` and `pre-push` git hooks
- Scaffolds `memory/` 3-drawer (STATE, semantic, decisions, learnings, episodic)
- Installs the router + `ai_runners/` executable AI overlay
- Adds `dharma` CLI wrapper at `.dharma/dharma`

**Requirements:** Python 3.9+, Git 2.0+, Bash. No external SDKs.

---

## Your first run

```bash
# 1. Classify a task — get a Route Receipt
.dharma/dharma route "add a chatbot that answers patient FAQs"

# Output:
# [Route B — New Feature]
#   Start:                 /intent
#   Overlays:              risk, ai
#   Forced gates:          /cso, /codex, /qa, /ai-economics, /ai-safety, /ai-observability
#   Exit evidence needed:  PRD contract; Plan complete; Evidence ledger

# 2. List all skills
.dharma/dharma skills

# 3. Inspect AI pricing
.dharma/dharma ai pricing

# 4. Suggest model for a task
.dharma/dharma ai suggest balanced   # → claude-sonnet-4-6

# 5. Try the evidence ledger
git commit -m "fix login: should work now"
# ✗ evidence-ledger: commit message contains banned phrase: "should work"

git commit -m "fix login: implemented and verified with tests/auth.spec.ts:42"
# ✓ accepted
```

---

## The 23 skills

| Phase | Skill | Role |
|---|---|---|
| **P0 Intent** | `/intent` | Product Partner — surface goal, success criteria, assumptions |
| | `/route` | Dispatcher — 7-step classifier; emits Route Receipt |
| **P1 Plan** | `/plan-ceo` | Founder — scope: Expansion / Selective / Hold / Reduction |
| | `/plan-eng` | Eng Manager — architecture, data flow, test matrix |
| | `/plan-design` | Senior Designer — rate 8 dimensions 0–10 |
| **P2 Design** | `/design-shotgun` | Design Explorer — 4–6 variants + taste learning |
| | `/design-build` | Design Engineer — mockup → production HTML |
| **P3 Build** | `/karpathy-check` | Discipline Gate — 4 questions before code |
| | `/investigate` | Debugger — reproduce → bisect → root cause |
| | `/review` | Staff Engineer — must-fix / nice-fix / note severity |
| **P4 Verify** | `/qa` | QA Lead — real-browser run + auto-regression tests |
| | `/cso` | Chief Security Officer — OWASP + STRIDE |
| | `/codex` | Cross-Model Adversarial Reviewer |
| | `/evidence` | Ledger Keeper — enforces completion language |
| **P5 Ship** | `/risk-gate` | Risk Overlay — forces gates on high-risk paths |
| | `/ship` | Release Engineer — sync, test, push, PR |
| | `/land-and-deploy` | Release Engineer — merge, deploy, verify health |
| | `/canary` | SRE — 30-min post-deploy monitoring |
| **P6 Learn** | `/retro` | Eng Manager — weekly reflection from episodic memory |
| | `/benchmark` | Performance Engineer — baseline + regression detection |
| **AI Overlay** | `/ai-economics` | AI Cost Architect — model selection, budget, ceiling |
| | `/ai-safety` | AI Safety Engineer — adversarial + injection + hallucination |
| | `/ai-observability` | AI SRE — telemetry, drift, refusal rate |

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│  OVERLAYS (always on, fire conditionally)                        │
│  • Risk Overlay  → auth/payments/AI/migrations → forced gates    │
│  • AI Overlay    → LLM features → economics + safety + obs       │
├─────────────────────────────────────────────────────────────────┤
│  P0 INTENT  →  P1 PLAN  →  P2 DESIGN  →  P3 BUILD               │
│       ↓                                                          │
│  P4 VERIFY  →  P5 SHIP  →  P6 LEARN  →  (loop)                  │
├─────────────────────────────────────────────────────────────────┤
│  INFRASTRUCTURE                                                  │
│  • 3-drawer memory (semantic / episodic / working STATE.md)     │
│  • Evidence ledger (banned-phrase enforcement)                  │
│  • Deterministic router (auto-classifies work → suggests skill) │
└─────────────────────────────────────────────────────────────────┘
```

Full details: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

---

## The AI overlay — the strategic moat

Dharma 1.0 is the first framework with first-class, executable LLM economics + safety + observability. **Pure-stdlib Python. 38 unit tests. Provider-agnostic.**

```python
from ai_runners import AIOverlay, EvalHarness, DriftDetector

# 1. Wrap any LLM — get cost tracking + telemetry for free
def my_llm(prompt: str) -> str:
    return openai_client.chat.completions.create(...).choices[0].message.content

overlay = AIOverlay(
    model_fn=my_llm,
    model_name="claude-sonnet-4-6",
    ceiling_usd=10.0,
    telemetry_path="logs/llm.jsonl",
)
response = overlay("Summarize this document...")
print(overlay.summary())
# {'calls': 1, 'total_cost_usd': 0.0087, 'status': 'ok', ...}

# 2. Run the safety eval against the same overlay
#    (eval costs are also tracked + logged)
harness = EvalHarness(model_fn=overlay, evals_dir="ai_runners/evals")
report = harness.run_all()
print(report.summary())
# {'overall_pass_rate': 0.92,
#  'categories': {
#    'jailbreak': {'pass': 5, 'fail': 0, 'rate': 1.0},
#    'injection': {'pass': 4, 'fail': 1, 'rate': 0.8},
#    ...}}

# 3. After deploy, detect distribution drift
print(DriftDetector("logs/llm.jsonl").detect(baseline_n=100, current_n=100))
# {'input_tokens': {'psi': 0.04, 'status': 'stable'},
#  'latency_ms':   {'psi': 0.31, 'status': 'significant'},
#  'overall_drift': True}
```

**Default eval set (extend as needed):**
- 5 jailbreak attempts (DAN, ignore-previous, role-play)
- 5 prompt-injection probes (canary tokens, tool-output abuse)
- 5 hallucination tests (3 factual + 2 honesty probes)
- 3 bias parity pairs (length + refusal disparity check)

**CLI:**
```bash
.dharma/dharma ai pricing                       # list pricing table
.dharma/dharma ai suggest balanced              # → claude-sonnet-4-6
.dharma/dharma ai summary logs/llm.jsonl        # p50/p95/p99 + cost + refusal rate
.dharma/dharma ai drift   logs/llm.jsonl        # PSI drift detection
.dharma/dharma ai eval    jailbreak             # inspect the eval set
```

---

## The evidence ledger

**Banned phrases at commit time** — no more "should work" PRs.

```bash
$ git commit -m "fix auth: should work now"

✗ evidence-ledger: commit message contains banned phrase: "should work"

  Use one of the 5 valid completion states instead:
    1. Implemented and verified with [evidence].
    2. Implemented but not runtime-verified — [what's missing].
    3. Planned only; no code changed.
    4. Partially complete; remaining risks: [list].
    5. Blocked: [specific blocker].
```

Banned phrases (extend in `.dharma/config.yaml`):
- "should work" / "should be fine" / "should pass"
- "probably works" / "probably passes"
- "I believe it's fixed" / "looks correct"
- "seems to work" / "appears correct"

---

## The deterministic router

7-step decision tree applied to a free-form task description. Stdlib-only Python. Auditable.

```bash
$ .dharma/dharma route "implement stripe billing for monthly subscription"

[Route B — New Feature]
  Task:                  implement stripe billing for monthly subscription
  Start:                 /intent
  Overlays:              risk
  Forced gates:          /cso, /codex, /qa
  Exit evidence needed:  PRD contract; Plan complete; Evidence ledger
```

The router never auto-executes a skill. It suggests. Human decides. Override is logged for tuning.

Tree details: [.dharma/routing-tree.md](.dharma/routing-tree.md).

---

## Comparison vs gstack and Dharma 0.x

| Axis | gstack | Dharma 0.x | **Dharma 1.0** |
|---|---|---|---|
| **Primary bet** | Roles → velocity | Gates → discipline | Roles + gates + evidence |
| **Skill count** | 23 | 38 | **23** |
| **Routing** | User picks | Deterministic tree | **Deterministic tree (auto-suggest)** |
| **Evidence enforcement** | None | Receipt template | **Commit-msg hook (banned phrases)** |
| **Risk overlay** | Opt-in | Route G | **Pre-push hook (forced gates)** |
| **AI as production layer** | No | Layer 6 (specs) | **Layer 6 (executable, tested)** |
| **Memory model** | One bucket (`/learn`) | 3 drawers (specs) | **3 drawers (working + semantic + episodic)** |
| **Real-browser QA** | Yes | Playwright | **Yes** |
| **Cross-model review** | `/codex` | None | **`/codex`** |
| **Deploy loop** | `/ship` → `/canary` | Stops at finish | **`/ship` → `/canary`** |
| **Install time** | ~minute | ~minute | **<1 second (verified)** |
| **License** | MIT | MIT | **MIT** |

---

## Repo structure

```
dharma-1/
├── README.md                  # this file
├── ETHOS.md                   # five principles, what we reject
├── CLAUDE.md                  # instructions for Claude Code
├── LICENSE                    # MIT
├── install.sh                 # 60-second installer
├── .dharma/
│   ├── config.yaml            # phases, overlays, banned phrases, triggers
│   └── routing-tree.md        # the 7-step classifier spec
├── skills/                    # 23 SKILL.md contracts across 6 phases + AI overlay
│   ├── p0-intent/{intent,route}/
│   ├── p1-plan/{plan-ceo,plan-eng,plan-design}/
│   ├── p2-design/{design-shotgun,design-build}/
│   ├── p3-build/{karpathy-check,investigate,review}/
│   ├── p4-verify/{qa,cso,codex,evidence}/
│   ├── p5-ship/{risk-gate,ship,land-and-deploy,canary}/
│   ├── p6-learn/{retro,benchmark}/
│   └── ai-overlay/{ai-economics,ai-safety,ai-observability}/
├── ai_runners/                # Executable AI overlay (the strategic moat)
│   ├── economics.py           # TokenTracker, pricing, ceilings
│   ├── safety.py              # EvalHarness, scorers
│   ├── observability.py       # JSONL emit, PSI drift, dashboard
│   ├── overlay.py             # Unified context manager
│   ├── cli.py                 # `python3 -m ai_runners.cli ...`
│   ├── evals/                 # jailbreak, injection, hallucination, bias
│   └── tests/                 # 38 unit tests
├── hooks/
│   ├── evidence-ledger.sh     # commit-msg hook
│   └── risk-overlay.sh        # pre-push hook
├── scripts/
│   └── router.py              # deterministic classifier
├── memory/_template/          # 3-drawer scaffold (STATE / semantic / episodic / decisions / learnings)
└── docs/
    ├── QUICKSTART.md
    └── ARCHITECTURE.md
```

---

## Status & roadmap

- ✅ **M1 — Foundation** (shipped): 23 skill contracts, 3-drawer memory, evidence-ledger hook, risk-overlay hook, deterministic router, 60-second installer.
- ✅ **M2 — AI overlay** (shipped): `economics.py` + `safety.py` + `observability.py` + `overlay.py` + CLI; 38 unit tests passing; default adversarial eval set.
- ✅ **M3 — Distribution** (partial): landing page live at https://sahudilip1356.github.io/dharma-1, Show HN drafts at [docs/SHOW_HN.md](docs/SHOW_HN.md). Pending: launch timing + optional telemetry.
- 🚧 **M2.5 — Dogfood**: install Dharma 1.0 in a real product repo, run `/route` on real tasks, fix what breaks first.
- 🚧 **M4 — Provider adapters**: drop-in adapters for OpenAI / Anthropic / Google SDKs so the overlay wires up in one line.

---

## Contributing

Pull requests welcome. Two rules:

1. **Stay in lane.** New skill must fill a documented gap in the 23-skill catalog. Default answer is "refine an existing skill," not "add a new one."
2. **Evidence over assertion.** PR body must use one of the five valid completion states. The commit-msg hook will reject banned phrases.

For non-trivial changes, open an issue first to align on scope.

---

## Lineage & acknowledgments

Dharma 1.0 stands on the shoulders of:

- **[gstack](https://github.com/garrytan/gstack)** by Garry Tan — the role/velocity model, real-browser QA, cross-model review, deploy loop.
- **[Dharma 0.x](https://github.com/SahuDilip1356/Dharma)** by Dilip Sahu — the evidence ledger, three-drawer memory, AI-as-production-system thesis, deterministic routing.
- **Andrej Karpathy** — the four failure modes (complexity, dependencies, simplicity, test-first) baked into `/karpathy-check`.
- **Boris Churney (Move Slow to Move Fast)** — the rhythm: P0 Intent + P1 Plan are non-negotiable, post-ship reflection closes the loop.

---

## License

MIT — fork freely, customize, contribute improvements back. See [LICENSE](LICENSE).

---

> **The framework that gets used wins. Dharma 1.0 gets used because it removes regret without removing speed.**
