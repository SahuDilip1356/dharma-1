# Show HN — launch copy drafts

Three variants. Pick the one that feels most "you" — or remix.

**Do not post yet.** Best timing is **Tue–Thu, 8:00–11:00 AM US Eastern**. Around then, the front-page churn is fastest and good posts have ~6 hours of daylight to climb.

Before posting, verify:
- [ ] Pages site loads cleanly on mobile + desktop
- [ ] README's "Your first run" section actually works on a fresh clone (one more dry run)
- [ ] You're around for the next 4 hours to answer comments — silence kills HN posts
- [ ] HN account is >2 weeks old with some prior comment karma (new accounts get auto-flagged)

---

## Variant A — Honest synthesis ("here's what I learned")

**Title** (76 chars):
```
Show HN: Dharma 1.0 – a framework to make Claude Code ship without regret
```

**URL**:
```
https://sahudilip1356.github.io/dharma-1/
```

**First comment (post immediately as the body):**

> I built Dharma 1.0 after a year of using AI coding assistants. They're fast. They're also undisciplined by default — same session that writes clean code will skip UX thinking, miss accessibility on user-facing screens, claim "it's done" based on belief, and ship LLM features with no token budget or adversarial test.
>
> These are process failures, not model failures.
>
> Dharma 1.0 is a synthesis. It takes [gstack](https://github.com/garrytan/gstack)'s role-based velocity model (CEO scopes, designer rates dimensions, QA opens a real browser) and adds a discipline spine: an evidence ledger (commit-msg hook rejects "should work"), a risk overlay (pre-push hook forces /cso + /codex + /qa when a diff touches auth/payments/migrations/AI), and the first executable AI overlay I'm aware of in a framework like this — token budgets, adversarial eval, drift detection, all stdlib Python, 38 unit tests.
>
> 23 skills, 6 phases, 60-second install. MIT. Stack-agnostic.
>
> Lineage credited in the README and on the landing page — gstack (Garry Tan), Dharma 0.x (my earlier project), Karpathy's four failure modes, Churney's "Move Slow to Move Fast."
>
> Honest about what's missing: provider adapters (OpenAI/Anthropic SDK wiring) is M4. Bias scoring is length/refusal parity only; semantic LLM-judge is deferred. The skill catalog files are markdown contracts — they tell Claude Code how to behave, but most aren't yet executable scripts.
>
> Would love brutal feedback on: (1) is "evidence ledger as commit hook" actually useful or just bureaucracy? (2) is the 23-skill count too many or too few? (3) what's missing from the AI safety eval set?

---

## Variant B — Lead with the moat (the AI overlay)

**Title** (74 chars):
```
Show HN: An executable AI safety + economics + observability overlay
```

**URL**:
```
https://github.com/SahuDilip1356/dharma-1
```

**First comment:**

> Most "AI agent frameworks" treat LLM features as if they were ordinary functions. They aren't. They have a token budget, a quality bar, a hallucination rate, a refusal pattern, and a cost ceiling — and these drift after deploy.
>
> Dharma 1.0 ships an executable AI overlay that fixes this. Drop-in wrapper:
>
> ```python
> overlay = AIOverlay(model_fn=my_llm, model_name="claude-sonnet-4-6",
>                    ceiling_usd=10.0, telemetry_path="logs/llm.jsonl")
> response = overlay("...")
> ```
>
> You get for free: cost tracking (8-model pricing table), budget alerts (80% / throttle / halt), JSONL telemetry, refusal-rate tracking, and PSI drift detection on input-token + latency distributions. Pure stdlib. Provider-agnostic. 38 unit tests.
>
> Plus an eval harness with default adversarial sets: 5 jailbreak prompts, 5 prompt-injection probes with canary tokens, 5 hallucination tests (3 factual + 2 honesty probes), 3 bias-parity pairs.
>
> ```python
> harness = EvalHarness(model_fn=overlay, evals_dir="ai_runners/evals")
> print(harness.run_all().summary())
> # {'overall_pass_rate': 0.92, 'categories': {...}}
> ```
>
> The overlay is part of a larger framework (23 skills across product → design → build → ship → learn, with an evidence-ledger commit hook and a risk-overlay pre-push hook), but the AI bits stand alone — you can `pip install` … well, not yet, that's next. For now it's MIT, clone-and-import.
>
> Would love feedback on the eval set design — what categories are missing? Tool-use abuse? Multi-turn jailbreaks?

---

## Variant C — Contrarian / sharp opinion

**Title** (78 chars):
```
Show HN: I cut my own 38-skill AI framework down to 23 and added a commit hook
```

**URL**:
```
https://sahudilip1356.github.io/dharma-1/
```

**First comment:**

> A year ago I built Dharma — a discipline-first framework for AI-assisted development with 38 skills across 8 layers, phase gates, evidence ledgers, the works.
>
> Then I built with it. And I noticed two things:
>
> 1. **The catalog was too big.** Skill selection became a meta-task. I'd spend 5 minutes deciding which of 5 nearly-identical uiux-* skills to invoke. Karpathy's simplicity-first applies to the framework itself — not just the code it produces.
>
> 2. **Discipline without speed doesn't survive contact with deadlines.** The framework was right but slow. Meanwhile [gstack](https://github.com/garrytan/gstack) (Garry Tan's) had the opposite problem — fast roles, no evidence enforcement, no AI-as-production-system layer.
>
> Dharma 1.0 is the synthesis. I cut my own framework 38 → 23 skills (no sacred cows, dropped the entire 11-skill uiux-* stack in favor of gstack's tighter 2-skill design loop), kept the spine (evidence ledger + risk overlay + 3-drawer memory), and shipped the executable AI overlay (token budgets, adversarial evals, drift detection, 38 unit tests, all stdlib).
>
> The evidence ledger is a commit-msg hook. Commit with "should work" or "probably passes" and it rejects you. Use one of five valid completion states ("implemented and verified with ..." / "implemented but not runtime-verified — ..." / "planned only" / "partially complete" / "blocked") and it accepts.
>
> 60-second install. MIT. Stack-agnostic.
>
> I'd love arguments against the cuts — especially: am I wrong that the uiux-* stack was bloat?

---

## After posting — engagement playbook

- **First 30 min:** reply to every comment, even the dismissive ones. Engagement velocity matters more than vote count in the ranking algorithm.
- **Don't be defensive.** Treat critiques as design notes. "Good point, here's what I was weighing — what would you do instead?" gets upvotes; defending is downvoted.
- **Don't reply to flamebait.** "This is just X" with no specifics → ignore or reply with one specific question.
- **Top of the hour rank checks** for the first 4 hours. If you're falling off /newest before hitting /front, it's a soft fail — not the end of the world.
- **Post-mortem regardless of outcome.** Log to `memory/learnings.md`: what surfaced, what didn't, who reached out, what to change next time.
