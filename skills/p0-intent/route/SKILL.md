---
name: route
phase: P0
role: Dispatcher
exit_evidence: Route Receipt emitted; overlays declared
description: Deterministic classifier. Reads task description, applies 7-step decision tree, suggests starting skill and active overlays.
---

# /route

**When to use:** Optional but recommended. Run immediately after `/intent` or as the very first action if intent is obvious.

**Logic:** See `.dharma/routing-tree.md` for the 7-step tree. Implemented in `scripts/router.py`.

**Inputs:**
- Task description (from `/intent` output or raw user prompt)
- Current `STATE.md` (if exists)

**Outputs (Route Receipt):**
```
[Route X] Task: <short summary>
Start: /<skill-name>
Overlays: [risk: yes/no, ai: yes/no]
Forced gates: [list]
Phase exit evidence required: [list]
```

**Exit gate:** Route Receipt printed and acknowledged. User can override but must do so explicitly.

**Override:** User types "override: route=<X>" to bypass classifier. Logged to `learnings.md` for future router tuning.
