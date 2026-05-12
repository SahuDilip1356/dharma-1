---
name: retro
phase: P6
role: Eng Manager
exit_evidence: Weekly retro doc written; ≥1 pattern promoted to semantic.md OR explicit "no patterns this week"
description: Reads episodic memory + decisions, surfaces patterns, writes weekly reflection. Closes the learning loop.
---

# /retro

**When to use:** Weekly (or end of sprint). Auto-triggered by `/canary` completion if no manual run in 7 days.

**Process:**
1. Read all `memory/episodic/YYYY-MM-DD-*.md` from last 7 days.
2. Read `memory/decisions.md` and `memory/learnings.md` deltas.
3. Read `/canary` outcomes from this period.
4. Identify:
   - **Shipping streak** — what shipped, what didn't, why
   - **Recurring failures** — same bug class twice? Promote to anti-pattern in `semantic.md`
   - **Recurring wins** — same approach worked twice? Promote to pattern in `semantic.md`
   - **Time leaks** — where did time go vs. plan
   - **Karpathy violations** — complexity added, tests skipped, root cause skipped

**Patterns get promoted** from episodic → semantic memory. Decay rate: 5%/week relevance.

**Inputs:** `memory/episodic/`, `decisions.md`, `learnings.md`, `canary` outputs.

**Outputs:**
- `memory/retros/YYYY-WW.md` — weekly summary
- Updates to `semantic.md` for promoted patterns

**Exit gate:** Retro file written. ≥1 actionable change for next week OR explicit "no changes needed".
