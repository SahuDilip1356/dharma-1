---
name: evidence
phase: P4
role: Ledger Keeper
exit_evidence: Evidence ledger entry signed; completion state matches one of five valid forms
description: Generates the evidence ledger receipt. Enforces completion language. Last gate before /ship.
---

# /evidence

**When to use:** Last skill in Phase 4. Required before `/ship` will run.

**The five valid completion states:**
1. "Implemented and verified with [specific evidence: test name, screenshot path, log excerpt]."
2. "Implemented but not runtime-verified — [what's missing: e.g., 'no staging access, will verify in canary']."
3. "Planned only; no code changed."
4. "Partially complete; remaining risks: [list]."
5. "Blocked: [specific blocker, who/what unblocks]."

**Banned phrases (rejected):**
- "should work" / "should be fine" / "should pass"
- "probably works" / "probably passes"
- "I believe it's fixed" / "looks correct"
- "seems to work" / "appears correct"

**Process:**
1. Read `STATE.md`, `/review` output, `/qa` output, `/cso` output, `/codex` output.
2. Synthesize claim using one of the 5 forms.
3. Attach evidence references (file:line, screenshot, log).
4. Write to `memory/evidence-[slug].md` AND append to `memory/decisions.md`.
5. Pre-commit hook `hooks/evidence-ledger.sh` will re-check at commit time.

**Inputs:** All Phase 4 outputs.

**Outputs:**
- `memory/evidence-[slug].md` — formal receipt
- Optional: PR body draft for `/ship`

**Exit gate:** Receipt uses valid state form. No banned phrases. Evidence references are file paths or URLs, not assertions.
