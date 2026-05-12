---
name: plan-eng
phase: P1
role: Engineering Manager
exit_evidence: Architecture diagram + data flow + test matrix + edge cases logged
description: Lock architecture, data flow, test matrix, edge cases, and DX friction. Engineering review before code.
---

# /plan-eng

**When to use:** After `/plan-ceo` (or after `/intent` for Route B). Mandatory before Phase 3 Build.

**Engineering checklist:**
1. **Architecture** — services, modules, file structure. Sketch ASCII or Mermaid.
2. **Data flow** — request → handler → store → response. Where does state live?
3. **Edge cases** — empty, error, loading, concurrent, malformed, malicious.
4. **Test matrix** — unit (which fns), integration (which boundaries), E2E (which flows).
5. **DX friction** — onboarding TTHW (time to "hello world"), local dev cost, deploy time.
6. **Dependencies** — new libraries needed? Why not existing? Bundle/security cost.

**Karpathy gate questions (also enforced in `/karpathy-check`):**
- Is this the simplest implementation that solves the problem?
- Are we adding a dependency where stdlib + 20 lines would suffice?
- Could a future you read this code 6 months from now?

**Inputs:** `memory/intent-[slug].md`, `memory/decisions.md`

**Outputs:**
- `memory/plan-[slug].md` with all 6 sections
- Update `STATE.md` next step
- Test matrix table

**Exit gate:** All 6 sections filled. ≥1 edge case identified per code path. Test matrix is non-empty.
