---
name: design-build
phase: P2
role: Design Engineer
exit_evidence: Production HTML/component delivered; matches approved variant; loads in real browser
description: Convert approved variant into production code. Real HTML or framework component, not Figma export.
---

# /design-build

**When to use:** After `/design-shotgun` produces an approved variant. Or directly after `/plan-design` if no variants needed.

**Standards:**
- Zero new dependencies unless justified in `/plan-eng`.
- Use design tokens (CSS variables) from `memory/semantic.md` if defined.
- All 4 states implemented: loading, empty, error, success.
- Responsive at 375 / 768 / 1280 px minimum.
- Accessible: keyboard nav, ARIA, contrast ≥4.5:1.

**Output rules:**
- Single component or page file (no premature splitting).
- Inline comments only where the *why* is non-obvious.
- No placeholder lorem ipsum — use realistic copy from `/intent`.

**Inputs:** Approved variant from `/design-shotgun` (or direction from `/plan-design`).

**Outputs:** Production component file(s) in target codebase.

**Exit gate:** Component renders in real browser at all 3 breakpoints. All 4 states visible. Keyboard tab order correct.

**Verification:** `/qa` will exercise this in Phase 4.
