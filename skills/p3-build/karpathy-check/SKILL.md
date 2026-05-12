---
name: karpathy-check
phase: P3
role: Discipline Gate
exit_evidence: Four questions answered yes/no with notes; ≥2 "no" answers blocks build
description: Pre-build discipline gate. Four Karpathy questions enforced — complexity, dependencies, simplicity, test-first.
---

# /karpathy-check

**When to use:** Mandatory before any non-trivial Phase 3 Build. Auto-invoked by `/review` if skipped.

**The four questions:**
1. **Complexity** — Am I adding complexity? If yes, can I delete equal complexity elsewhere?
2. **Dependencies** — Am I adding a dependency where stdlib + 20 lines would suffice? Could this be a function instead of a package?
3. **Simplicity** — Is this the simplest implementation that solves the *actual* problem? Or am I solving an imagined future problem?
4. **Test-first** — Is there a failing test that this code will make pass? If not, why not?

**Scoring:**
- All 4 "yes" → proceed.
- 1 "no" with note → proceed with warning.
- ≥2 "no" → **build blocked**. Return to `/plan-eng` or simplify scope.

**Inputs:** Current plan from `memory/plan-[slug].md` + proposed implementation summary.

**Outputs:**
- `memory/karpathy-check-[slug].md` — 4 Q/A with notes
- Update `STATE.md` next step

**Exit gate:** ≤1 "no" answer.
