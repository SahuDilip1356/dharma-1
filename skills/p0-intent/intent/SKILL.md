---
name: intent
phase: P0
role: Product Partner
exit_evidence: PRD contract committed; assumptions surfaced and listed
description: Open the work cycle. Surface the goal, success criteria, assumptions, and scope. Output a durable PRD contract that later phases cite.
---

# /intent

**When to use:** First skill for any new product, feature, or non-trivial change. Mandatory for Route A and Route B.

**Six forcing questions:**
1. Who is this for? (user persona, role, context of use)
2. What problem is solved? (in their words, not yours)
3. What's the success criterion? (observable, measurable)
4. What's explicitly *out of scope*? (the things you will not build)
5. What are you assuming that might be wrong? (≥3 assumptions)
6. What's the rollback plan if this is the wrong bet?

**Inputs:** User's natural-language task description.

**Outputs:**
- `memory/intent-[slug].md` — PRD contract with the 6 answers
- Update `STATE.md` with current intent + open assumptions

**Exit gate:** All six questions answered. ≥3 assumptions logged. Success criterion is observable (not "feels good").

**Routes downstream:** `/route` → `/plan-ceo` (new product) or `/plan-eng` (new feature).
