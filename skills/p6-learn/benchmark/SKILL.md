---
name: benchmark
phase: P6
role: Performance Engineer
exit_evidence: Baseline captured; before/after delta logged; regression alert if >10%
description: Performance baselining and regression detection. Core Web Vitals + custom metrics. Before/after comparison.
---

# /benchmark

**When to use:** Route F (performance work). Optional but recommended after any change touching hot paths, bundle size, or AI inference.

**Default metrics (web):**
- LCP, FID/INP, CLS (Core Web Vitals)
- TTFB, FCP
- Bundle size (gzipped)
- Lighthouse score

**Default metrics (AI features):**
- Latency p50/p95/p99 per LLM call
- Token usage (input + output)
- Cost per request
- Cache hit rate (if applicable)
- Quality score (if eval set configured)

**Process:**
1. Capture baseline on `main` (or pre-change commit).
2. Capture post-change measurement on current branch.
3. Diff. Anything >10% regression → block `/ship` until acknowledged.
4. Anything >25% improvement → log to `semantic.md` as pattern.

**Inputs:** Target URL or endpoint + metric set.

**Outputs:**
- `memory/benchmark-[slug].md` — baseline, current, delta
- Update `STATE.md`

**Exit gate:** Delta logged. No silent regressions.
