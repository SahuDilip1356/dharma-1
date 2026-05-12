---
name: land-and-deploy
phase: P5
role: Release Engineer
exit_evidence: PR merged; deploy completed; production health check green
description: Merge PR, wait for CI, deploy, verify production health.
---

# /land-and-deploy

**When to use:** After `/ship` produces a green PR and reviewer approval (human or auto-approve policy).

**Steps:**
1. Verify PR has required approvals per repo policy.
2. Merge via `gh pr merge --squash` (or repo's preferred strategy).
3. Watch CI on `main` until deploy job starts.
4. Watch deploy job until target environment is green.
5. Hit production health-check endpoint(s). Block on non-200.
6. Smoke-test the changed feature in production (or staging if no prod yet).
7. Update `memory/decisions.md` with deploy timestamp + commit SHA.
8. Auto-invoke `/canary` for the next 30 minutes.

**Failure protocol:**
- CI fails post-merge → escalate, suggest revert via `gh pr create --base main`.
- Health check fails → auto-suggest rollback. Do not auto-rollback without user confirmation.

**Inputs:** PR URL from `/ship`.

**Outputs:** Deploy receipt with timestamps, SHA, environment URL.

**Exit gate:** Production health check green. `/canary` started.
