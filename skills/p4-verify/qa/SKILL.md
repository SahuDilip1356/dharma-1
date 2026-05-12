---
name: qa
phase: P4
role: QA Lead
exit_evidence: Real-browser run completed; bugs filed OR clean pass; regression test added for each bug
description: Real-browser exercise of the changed feature. Auto-generates regression tests for any bug found.
---

# /qa

**When to use:** Mandatory before `/ship` for any user-facing change. Auto-triggered by risk overlay.

**Process:**
1. Open real Chromium (not jsdom) at dev URL.
2. Exercise the golden path of the changed feature.
3. Exercise edge cases from `/plan-eng` test matrix.
4. Check all 4 states (loading, empty, error, success).
5. Test responsive at 375 / 768 / 1280.
6. Test keyboard nav + screen reader landmark order.
7. Run on Chrome, Safari, Firefox if available.

**Bug protocol:** Every bug found gets a regression test added before fix. Fix lands with the test.

**Flags:**
- `--report-only` — find bugs, write report, do not fix (replaces gstack `/qa-only`)
- `--devex` — time the onboarding flow; screenshot every error

**Inputs:** Dev server URL, feature path/route, plan test matrix.

**Outputs:**
- `memory/qa-report-[slug].md` — bugs found, screenshots, repro steps
- `tests/regression/[bug-id].spec.ts` — one test per bug
- Update `STATE.md`

**Exit gate:** Zero unresolved must-fix bugs. All bugs have regression tests committed.
