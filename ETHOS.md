# Dharma 1.0 — Ethos

## The five principles

1. **Role gives velocity.** Skills are personas with decision frameworks, not generic prompts. Designer designs. QA tests. CEO scopes.

2. **Evidence replaces belief.** "Should work" is banned. Five completion states only: *verified | implemented-not-verified | planned-only | partial | blocked*.

3. **Gate before advancing.** Each phase has exit evidence. The router checks it before letting you move forward — never silently.

4. **Risk overlays trump speed.** Auth, payments, AI safety, migrations, compliance — these always trigger extra gates regardless of work type. No exceptions.

5. **AI features are production systems.** LLM-powered work requires dedicated economics, adversarial safety eval, and post-ship observability. Not optional.

## What we reject

- **Vibes-based skill selection.** The router classifies first; you pick second.
- **LOC velocity claims without verified shipping.** Logical-LOC is a vanity metric without `/canary` confirming production health.
- **Process theater.** Gates that never catch issues get dropped. Measure or remove.
- **38-skill catalogs.** Karpathy's simplicity-first applies to the framework itself. 23 is the ceiling.
- **Hidden complexity.** No magic. Every hook is readable. Every gate is auditable.

## The four Karpathy modes we defend against

1. **Over-complexity** — `/karpathy-check` before build; `/plan-eng` locks architecture.
2. **Missing dependencies** — `/intent` surfaces assumptions as durable contract.
3. **Starting non-simple** — `/simplicity-first` heuristic in `/review`.
4. **Test-after-code** — `/qa` auto-generates regression per fix; `/evidence` rejects un-run claims.

## The Churney rhythm

- **Move slow to move fast.** P0 Intent + P1 Plan are non-negotiable for new features. The 20 minutes spent here save 4 hours later.
- **Design Review Gate** — `/plan-design` rates 0–10 before code is written.
- **Post-ship reflection** — `/retro` reads episodic memory weekly. Patterns become semantic memory.

## The Tan distribution principle

- **60-second install.** If `./install.sh` takes longer, we cut features until it doesn't.
- **Invisible until violated.** Gates don't slow you down — they catch you when you'd otherwise crash.
- **Open-source, MIT, no premium tier.** Forks > customers.

---

*The framework that gets used wins. Dharma 1.0 gets used because it removes regret without removing speed.*
