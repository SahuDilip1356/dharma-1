---
name: risk-gate
phase: P5
role: Risk Overlay
exit_evidence: Risk overlay verdict logged; if triggered, all forced gates have green receipts
description: Pre-/ship overlay. Scans diff for high-risk paths. Forces /cso + /codex + /qa if triggered.
---

# /risk-gate

**When to use:** Automatic. Invoked by `/ship` before any merge. Cannot be bypassed.

**Trigger paths** (from `.dharma/config.yaml`):
- `auth/`, `**/auth/**`
- `payments/`, `**/billing/**`
- `migrations/`, `**/*.sql`
- `prompts/`, `**/llm/**`, `**/agents/**`
- `*.policy.*`, `**/permissions/**`

**Logic:**
1. Run `git diff --name-only $BASE...HEAD` against trigger list.
2. If ≥1 path matches → high-risk diff detected.
3. Check `memory/` for valid `/cso`, `/codex`, `/qa` receipts in last 24h on this branch.
4. Missing receipt → `/ship` blocked. Tell user which gate to run.

**Bypass:** Only by explicit override flag with logged justification. Goes to `learnings.md` for audit.

**Inputs:** Current git diff vs base branch.

**Outputs:**
- Verdict: PASS | BLOCK
- Block reason if applicable
- Append to `memory/risk-gate-log.md`

**Exit gate:** PASS verdict OR documented bypass.
