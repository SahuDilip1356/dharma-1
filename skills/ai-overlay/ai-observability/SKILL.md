---
name: ai-observability
phase: P5 (overlay)
role: AI SRE
exit_evidence: Telemetry wired; dashboards link in PR; drift detector configured
description: Post-ship LLM monitoring. Latency, cost, quality, drift, refusal rate, hallucination rate. Required before AI features go live.
---

# /ai-observability

**When to use:** Auto-triggered by AI overlay before `/land-and-deploy`. Wires monitoring before code goes live.

**Five always-on metrics:**

**1. Latency** — p50/p95/p99 per endpoint per model. Alert on >1.5× baseline.

**2. Cost** — $ per request, $ per user/day, $ per feature. Alert at 80% of ceiling from `/ai-economics`.

**3. Quality** — eval set score over time. Re-run sampled prompts daily; alert on >10% drop.

**4. Drift** — input distribution change detection. New token patterns, unusual lengths, new language mix. Alert on KL divergence >threshold.

**5. Safety** — refusal rate, jailbreak attempts blocked, hallucination eval score. Alert on anomalies.

**Implementation:**
- Emit structured logs per LLM call: `{request_id, model, input_tokens, output_tokens, latency_ms, cost_usd, eval_score?, refusal?}`
- Pipe to observability backend (LangSmith, LangFuse, Helicone, custom)
- Dashboards: link committed in PR body

**Drift detection:** Lightweight in-process anomaly check on rolling window. Falls back to scheduled job if no streaming infra.

**Inputs:** `/ai-economics` ceilings, deploy target.

**Outputs:**
- Telemetry code in feature
- `memory/ai-obs-[slug].md` — dashboard URLs, alert thresholds, on-call

**Exit gate:** Telemetry deployable. Dashboards reachable. Alerts route to owner.

---

## Implementation

Executable code in [ai_runners/observability.py](../../../ai_runners/observability.py). Pure-stdlib JSONL emit + PSI drift detection (no backend required).

```python
from ai_runners import AIOverlay, Dashboard, DriftDetector

# Option 1: use AIOverlay — wraps any model_fn, auto-emits telemetry per call
overlay = AIOverlay(
    model_fn=my_model,
    model_name="claude-sonnet-4-6",
    telemetry_path="logs/llm.jsonl",
    ceiling_usd=10.0,
)
response = overlay("Summarize this document...")

# Option 2: manual emit
from ai_runners import TelemetryEmitter
TelemetryEmitter("logs/llm.jsonl").emit(
    model="claude-sonnet-4-6",
    input_tokens=1200, output_tokens=340,
    latency_ms=850, cost_usd=0.0087,
)

# Read back as dashboard
print(Dashboard("logs/llm.jsonl").summary())
# {'count': 100, 'latency_ms': {'p50': 420, 'p95': 1200, ...}, 'cost_usd': {...}}

# Detect drift (PSI) between baseline and current windows
print(DriftDetector("logs/llm.jsonl").detect(baseline_n=100, current_n=100))
# {'input_tokens': {'psi': 0.04, 'status': 'stable'},
#  'latency_ms': {'psi': 0.31, 'status': 'significant'},
#  'overall_drift': True}
```

**Drift thresholds:** PSI <0.10 stable, 0.10–0.25 moderate, >0.25 significant.

**CLI:**
```bash
python3 -m ai_runners.cli summary logs/llm.jsonl
python3 -m ai_runners.cli drift   logs/llm.jsonl --baseline 100 --current 100
```

**Pipe to your backend (optional):** the JSONL is shipped-ready for LangSmith / LangFuse / Helicone / custom — they all accept structured logs.
