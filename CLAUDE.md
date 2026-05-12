# Dharma 1.0 — Project Instructions for Claude Code

## What this repo is
The Dharma 1.0 framework — 22 skills, 6 phases, 2 overlays, 60-second install.

## Skill discovery
All skills live under `skills/<phase>/<skill-name>/SKILL.md`. The router (`scripts/router.py`) maps a task description to a suggested skill.

## Mandatory pre-flight (every skill)
1. Load `memory/_template/STATE.md` if working on a real project, else skip.
2. Read the phase's exit-evidence requirement (in SKILL.md frontmatter).
3. If a previous phase's evidence is missing, surface it before proceeding.

## Completion language — enforced
Only these five states are valid:
1. Implemented and verified with [evidence].
2. Implemented but not runtime-verified — [what's missing].
3. Planned only; no code changed.
4. Partially complete; remaining risks: [list].
5. Blocked: [specific blocker].

Banned: "should work", "probably passes", "I believe it's fixed", "looks correct".

The `hooks/evidence-ledger.sh` pre-commit hook will reject commits whose message contains banned phrases.

## Risk overlay — automatic
Any diff touching these paths triggers forced gates before `/ship`:
- `auth/`, `**/auth/**`
- `payments/`, `**/billing/**`
- `migrations/`, `**/*.sql`
- `prompts/`, `**/llm/**`, `**/agents/**`
- `*.policy.*`, `**/permissions/**`

Forced gates: `/cso` + `/codex` + `/qa` (no opt-out).

## Standards
- Skills stay in lane. Discoveries out-of-scope → escalate to user, never absorb.
- New skills require a documented gap in the 22-skill catalog. Default answer is "no, refine an existing skill."
- All hooks are readable shell or Python. No compiled binaries in v1.0.

## License
MIT. Co-author lineage required in commits: gstack (Garry Tan), Dharma 0.x (Dilip Sahu).
