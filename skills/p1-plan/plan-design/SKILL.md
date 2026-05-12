---
name: plan-design
phase: P1
role: Senior Designer
exit_evidence: Design dimensions rated 0–10; <7 ratings have improvement plan
description: Rate design across 8 dimensions before code. Catch slop before it ships.
---

# /plan-design

**When to use:** Mandatory for user-facing features (Route B with UX surface, Route D). Optional for backend-only.

**Eight design dimensions (rate 0–10 each):**
1. **Information hierarchy** — what's the first thing the eye lands on?
2. **State coverage** — loading, empty, error, success all designed?
3. **Typography rhythm** — ≤3 sizes, ≤2 weights, consistent line-height?
4. **Color discipline** — primary, neutral, semantic only? No random hex codes?
5. **Spacing system** — uses tokens (4/8/16/24), not arbitrary px?
6. **Interaction feedback** — hover, focus, active, disabled all distinct?
7. **Copy quality** — labels are verbs/nouns, errors actionable, no jargon?
8. **Accessibility** — color contrast ≥4.5:1, keyboard reachable, ARIA correct?

**Rating bar:** any score <7 must have an improvement note. Average <8 → return to design before build.

**Inputs:** Mockup or design spec (URL, image, or written description).

**Outputs:**
- `memory/design-rating-[slug].md` with 8 scores + notes
- Update `STATE.md`

**Exit gate:** All 8 rated. Average ≥8 OR explicit override logged.
