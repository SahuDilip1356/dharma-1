---
name: ai-economics
phase: P1 (overlay)
role: AI Cost Architect
exit_evidence: Model selected with rationale; token budget set; cost ceiling defined; cache strategy declared
description: Model selection, token budget, cost ceiling. Mandatory for any LLM-touching feature before build.
---

# /ai-economics

**When to use:** Auto-triggered by AI overlay when diff touches `**/llm/**`, `**/prompts/**`, `**/agents/**`, `**/embeddings/**`. Runs in Phase 1.

**Four decisions:**

**1. Model selection** — for each task, pick the smallest model that meets quality bar.
- Cheap/fast: Haiku, Gemini Flash, GPT-4 mini
- Balanced: Sonnet, Gemini Pro
- Expensive: Opus, GPT-5
- Document: which task → which model → why not the tier below

**2. Token budget**
- Input ceiling per call (prompt + context)
- Output ceiling per call (max_tokens)
- Total budget per session (concurrent context buildup)
- Compaction strategy if approaching ceiling

**3. Cost ceiling**
- Cost per request (target + hard cap)
- Cost per user/day (target + hard cap)
- Trigger: alert at 80%, throttle at 100%, halt at 120%

**4. Cache strategy**
- Prompt cache enabled? (Anthropic-native or app-level)
- Cache hit target (e.g., ≥70% on common prompts)
- Eviction policy

**Inputs:** Feature description from `/intent`, `/plan-eng` data flow.

**Outputs:** `memory/ai-economics-[slug].md` — four decisions documented.

**Exit gate:** All 4 sections filled. Cost ceiling has a number, not "tbd".

---

## Implementation

Executable code in [ai_runners/economics.py](../../../ai_runners/economics.py):

```python
from ai_runners import TokenTracker, suggest_model

# Decision 1: model selection — get a starting suggestion
model = suggest_model("balanced")  # → "claude-sonnet-4-6"

# Decision 2-3: token budget + cost ceiling
tracker = TokenTracker(ceiling_usd=10.00, alert_at=0.80, throttle_at=1.00, halt_at=1.20)

# Per-call usage
tracker.record(model, input_tokens=1200, output_tokens=340)

# Status checks
if tracker.over_budget():
    raise SystemExit("budget exceeded — halt before further spend")

print(tracker.summary())
# {'calls': 1, 'total_cost_usd': 0.0087, 'status': 'ok', ...}
```

**CLI:**
```bash
python3 -m ai_runners.cli pricing             # list pricing table
python3 -m ai_runners.cli suggest balanced    # → claude-sonnet-4-6
```

**Pricing table:** `ai_runners/economics.py` PRICING dict. Update as providers change.
