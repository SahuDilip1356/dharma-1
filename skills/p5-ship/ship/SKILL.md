---
name: ship
phase: P5
role: Release Engineer
exit_evidence: Branch pushed; PR opened with evidence ledger in body; CI green
description: Sync, test, push, open PR. PR body auto-populated from evidence ledger.
---

# /ship

**When to use:** After all Phase 4 gates have green receipts.

**Steps:**
1. Run `/risk-gate` — block if forced gates missing.
2. Fetch + rebase against base branch. Resolve conflicts (escalate if non-trivial).
3. Run test suite locally. Block on failure.
4. Run lint + typecheck. Block on errors (not warnings).
5. Push branch.
6. Open PR via `gh pr create`. Body = evidence ledger from `/evidence`.
7. Wait for CI to start. Confirm green ≤10min OR escalate.
8. Auto-update `memory/decisions.md` with PR URL + date.

**PR body template:**
```
## Summary
[from /intent goal]

## Evidence
[from /evidence — the 5-state claim with references]

## Risk Gate
[from /risk-gate — PASS or bypass justification]

## Review
[/review must-fixes resolved, /codex verdict]

## QA
[/qa report link, regression tests added]

## Rollback
[1-line plan if this needs to be reverted]
```

**Auto-runs:** `/document-release` step folded in (updates README, CHANGELOG, ARCHITECTURE if changed).

**Inputs:** All Phase 4 receipts.

**Outputs:** Pushed branch, open PR with full body. PR URL printed.

**Exit gate:** PR open + CI green.
