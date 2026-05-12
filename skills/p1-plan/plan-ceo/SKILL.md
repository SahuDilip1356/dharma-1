---
name: plan-ceo
phase: P1
role: Founder / CEO
exit_evidence: Scope decision logged (Expansion | Selective | Hold | Reduction) with rationale
description: Rethink scope before code. Four modes — Expansion, Selective, Hold, Reduction. Force trade-offs explicit.
---

# /plan-ceo

**When to use:** After `/intent`, before architecture. Mandatory for Route A (new product). Optional but recommended for Route B (new feature) if scope is fuzzy.

**Four scope modes:**
- **Expansion** — what would 2× this idea look like? Why aren't we doing that?
- **Selective** — what's the smallest version that proves the bet?
- **Hold** — what would make us stop and ship the existing system instead?
- **Reduction** — what can we cut and still have something worth shipping?

**Forcing questions:**
1. What's the wedge? (the single thing this does better than alternatives)
2. What's the riskiest assumption? (and how do we test it in <1 week?)
3. Who would use this in 30 days? Name them or admit you don't know.
4. What's the unit economics? Does it work at 10×?

**Inputs:** `memory/intent-[slug].md`

**Outputs:**
- Append scope decision to `memory/decisions.md`
- Update `STATE.md` with scope mode

**Exit gate:** One of the four modes is chosen. Rationale logged. Alternatives rejected with why-not.
