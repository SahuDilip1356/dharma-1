---
name: canary
phase: P5
role: SRE
exit_evidence: 30-minute post-deploy window monitored; no regressions OR rollback initiated
description: Post-deploy monitoring. Console errors, perf regressions, error rate spikes, failure modes.
---

# /canary

**When to use:** Auto-invoked by `/land-and-deploy`. Runs for 30 minutes by default.

**Watches:**
- Error rate vs. 7-day baseline (>2× = alert)
- p95 latency vs. baseline (>1.5× = alert)
- Console errors in real browser sampling
- Failed background jobs / queue depth
- Auth failure rate, payment failure rate (if applicable)
- LLM-specific: hallucination rate, refusal rate, cost burn (if AI overlay active)

**Action on alert:**
1. Print alert with metric, baseline, current value.
2. Suggest rollback command but do not execute.
3. Wait for user decision.

**Inputs:** Deploy timestamp + SHA from `/land-and-deploy`.

**Outputs:**
- `memory/canary-[sha].md` — 30-minute summary
- Append to `memory/decisions.md` (deploy outcome)

**Exit gate:** 30-minute window completed. Status: GREEN | YELLOW (note in learnings) | RED (rollback recommended).

**Note:** Requires observability connection (config in `.dharma/config.yaml`). Falls back to log-tailing if no metrics endpoint.
