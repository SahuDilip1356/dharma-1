---
name: investigate
phase: P3
role: Debugger
exit_evidence: Root cause identified; reproduction confirmed; fix tested OR three failed attempts logged
description: Systematic root-cause analysis. Reproduce first, theorize second, fix third. Stops after 3 failed attempts.
---

# /investigate

**When to use:** Route C (bug fix). Anytime symptoms appear without a clear cause.

**Five-step process:**
1. **Reproduce** — get the bug to happen reliably. If you can't reproduce, stop and gather more data.
2. **Bisect** — narrow the scope (which commit, which input, which user, which env).
3. **Theorize** — write ≥2 hypotheses for root cause before testing any.
4. **Test cheapest first** — verify or kill each hypothesis with the smallest experiment.
5. **Fix at root** — not at symptom. If you're patching the surface, label it as a known limitation.

**Stop conditions:**
- 3 failed fix attempts → escalate to user; do not keep trying.
- Symptom resolves but root cause unknown → log as `learnings.md` entry "fixed but cause unclear".

**Inputs:** Error message, stack trace, repro steps, recent commits.

**Outputs:**
- `memory/learnings.md` entry (root cause, fix, generalization, prevention)
- Fix code OR escalation note

**Exit gate:** Root cause documented OR escalation logged. Symptom no longer reproduces.
