---
name: review
phase: P3
role: Staff Engineer
exit_evidence: All findings categorized (must-fix | nice-fix | note); must-fixes resolved or escalated
description: Production-bug detection on the current diff. Auto-fixes obvious issues; flags rest.
---

# /review

**When to use:** After Build, before `/qa`. Mandatory before `/ship` for any non-trivial change.

**Checks (in order of severity):**

**Must-fix (block merge):**
- N+1 queries, missing indexes on hot paths
- Unhandled error paths (especially in async / network code)
- Race conditions, missing locks, double-fire on form submit
- SQL injection, XSS, command injection, path traversal
- Hardcoded secrets, API keys, tokens
- Missing auth checks on protected routes

**Nice-fix (warn, allow merge):**
- Code duplication >3 occurrences without abstraction
- Functions >50 lines without clear single responsibility
- Magic numbers without named constants
- Dead code, unused imports, unused exports

**Note (informational):**
- React-specific: re-renders, missing keys, useEffect cleanup
- Bundle size additions
- Imperative loops where map/filter would read clearer

**Inputs:** `git diff` against base branch.

**Outputs:**
- Inline comments on diff
- `memory/review-[slug].md` summary
- Auto-fix commits for trivial issues (whitespace, unused imports)

**Exit gate:** Zero must-fix findings unresolved.
