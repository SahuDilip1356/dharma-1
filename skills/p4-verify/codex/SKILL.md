---
name: codex
phase: P4
role: Adversarial Reviewer (Cross-Model)
exit_evidence: Independent model verdict logged (pass | fail | adversarial-findings); disagreements resolved
description: Second-opinion review by an independent model (OpenAI Codex / GPT). Catches single-model bias.
---

# /codex

**When to use:** Mandatory by risk overlay (auth/payments/AI/migrations). Recommended for any change >100 LoC.

**Modes:**
- **Pass/fail gate** — independent model approves or rejects. Disagreement with Claude = surface to user.
- **Adversarial** — explicitly ask the second model to find what Claude missed. Hostile critique mode.

**Process:**
1. Package the diff + relevant context (plan, intent, review findings).
2. Send to OpenAI Codex CLI or chosen alternative model.
3. Compare verdict against Claude's `/review` output.
4. Disagreements logged with both sides' reasoning.

**Requires:** `OPENAI_API_KEY` env var, or alternative model configured in `.dharma/config.yaml`.

**Inputs:** `git diff`, `memory/review-[slug].md`, `memory/plan-[slug].md`.

**Outputs:**
- `memory/codex-review-[slug].md` — second-model verdict + adversarial findings
- Disagreements flagged for user resolution

**Exit gate:** Verdict logged. Any "fail" or unresolved disagreement blocks `/ship`.
