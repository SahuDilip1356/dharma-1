# Deterministic Routing Tree

The router (`scripts/router.py`) reads the user's task description and applies this tree top-down. First match wins.

## 7-step classification

1. **Risk surface check** → does the task mention `auth`, `payment`, `billing`, `migration`, `prompt`, `agent`, `LLM`, `policy`, `permission`?
   → Apply **Risk Overlay**: forced `/cso + /codex + /qa` before `/ship`.

2. **AI feature check** → does the task involve LLM/embeddings/agents/prompts?
   → Apply **AI Overlay**: forced `/ai-economics` (plan) + `/ai-safety` (build) + `/ai-observability` (ship).

3. **Bug / fix language** → "fix", "broken", "not working", "regression"?
   → Route C: start at `/investigate` (root cause before fix).

4. **New product / 0→1 language** → "build a new", "from scratch", "MVP for"?
   → Route A: start at `/intent` → `/plan-ceo`.

5. **New feature in existing product** → "add", "implement", "new screen"?
   → Route B: start at `/intent` → `/plan-eng` (UX gate if user-facing).

6. **UI/UX-only** → "redesign", "visual", "layout", "design system"?
   → Route D: start at `/design-shotgun`.

7. **Refactor / performance / security** → behavior-preserving change?
   → Route E/F/G: start at `/karpathy-check` (refactor) or `/benchmark` (perf) or `/cso` (security).

## Default

If none match → Route B (new feature), start at `/intent`.

## Output: Route Receipt

The router emits a one-line receipt:

```
[Route X] Task: <short> → Start: /<skill>. Overlays: [risk?, ai?]. Phase exit evidence required: <list>.
```
