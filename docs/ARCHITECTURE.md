# Dharma 1.0 — Architecture

## Three layers

```
┌────────────────────────────────────────────────────────┐
│                  CONTROL                               │
│  • Router (scripts/router.py)                          │
│  • Evidence ledger hook (hooks/evidence-ledger.sh)     │
│  • Risk overlay hook (hooks/risk-overlay.sh)           │
│  • Config (.dharma/config.yaml)                        │
├────────────────────────────────────────────────────────┤
│                  SKILLS                                │
│  6 phases × 2–4 skills each + AI overlay (3 skills)    │
│  Each skill = SKILL.md with role + exit_evidence       │
├────────────────────────────────────────────────────────┤
│                  MEMORY                                │
│  STATE.md (working) ← read by every skill              │
│  semantic.md (durable patterns + taste)                │
│  decisions.md (append-only, with rationale)            │
│  learnings.md (append-only, failures + fixes)          │
│  episodic/ (per-session digests)                       │
└────────────────────────────────────────────────────────┘
```

## How a skill runs

1. **Pre-flight** — skill reads `STATE.md` + `semantic.md`. If phase prereq evidence missing → surface to user.
2. **Execution** — skill applies its role-specific logic (questions, checks, generations).
3. **Output** — skill writes to its designated memory file (e.g., `intent-[slug].md`, `plan-[slug].md`).
4. **Exit gate** — skill self-checks its `exit_evidence` requirement. Fails → mark partial, don't advance phase.
5. **Post-flight** — `STATE.md` updated with phase, next step. Significant decisions appended to `decisions.md`.

## How the router runs

1. User types task description (free-form).
2. Router applies 7-step decision tree (see `.dharma/routing-tree.md`).
3. Risk + AI overlays detected via keyword/regex match.
4. Route Receipt printed: route, starting skill, overlays, forced gates, exit evidence.
5. User can override; override is logged for router tuning.

The router never auto-executes a skill. It suggests. The human decides.

## How the hooks run

**commit-msg (evidence ledger):**
- Reads the commit message.
- Rejects on banned phrases ("should work", etc.).
- Warns if no valid completion state phrase present (non-blocking).

**pre-push (risk overlay):**
- Diffs against base branch.
- If diff touches `auth/`, `payments/`, `migrations/`, `prompts/`, `policy.*` etc. → checks `memory/` for fresh `/cso`, `/codex`, `/qa` receipts.
- Missing receipts → push blocked.
- `DHARMA_RISK_BYPASS="<justification>"` env var bypasses with audit trail in `learnings.md`.

## Memory model details

**Working memory (STATE.md):** Single file, mutable, ≤200 lines. Source of truth for "where am I right now."

**Semantic memory (semantic.md):** Long-lived. Domain glossary, taste, anti-patterns. Surfaced into every skill pre-flight.

**Decisions:** Append-only. Each entry: context, options considered, choice, rationale, alternatives rejected, reversal cost.

**Learnings:** Append-only. Each entry: symptom, root cause, fix, generalization, prevention.

**Episodic:** Per-session digest files. Mined by `/retro` weekly. Patterns promoted to `semantic.md`.

**Staleness check:** Files >7 days old surface a one-line warning when read. Never blocks.

## Extension points

- **New skill:** Add `skills/<phase>/<name>/SKILL.md` with frontmatter (`name`, `phase`, `role`, `exit_evidence`, `description`). Lives next to existing skills.
- **New route:** Add to `.dharma/routing-tree.md` AND `scripts/router.py` keyword list.
- **New risk trigger:** Add to `risk.triggers` in `.dharma/config.yaml` AND `hooks/risk-overlay.sh` regex.
- **New banned phrase:** Add to `completion_language.banned_phrases` in config AND `hooks/evidence-ledger.sh` BANNED array.

## What this is not

- Not a code generator — humans + LLMs write code; Dharma controls *when* and *with what evidence*.
- Not a CI/CD replacement — `/ship` calls `gh` and your existing CI. Dharma is the pre-flight + monitor layer.
- Not an agent framework — no autonomous loops. Every skill is a deliberate human invocation.
- Not framework-locked — works with any stack (React/Vue, Node/Python/Go, etc.).
