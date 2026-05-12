# Dharma 1.0

**Build with role. Ship with evidence. Govern with intention.**

A unified framework for AI-assisted product development. The synthesis of gstack's velocity (roles, real-browser QA, deploy loop) and Dharma's discipline (evidence ledger, risk overlay, AI-native governance).

23 skills. 6 phases. 2 always-on overlays. 60-second install.

---

## Why Dharma 1.0

- **gstack** ships fast. **Dharma 0.x** ships safely. Neither does both.
- Dharma 1.0 is the smallest framework that ships fast *and* doesn't regret it.
- AI-native by default — first framework with first-class LLM economics, safety, and observability.
- Evidence enforced — "should work" is banned at PR time.
- Risk-aware — diff touches auth/payments/AI/migrations → forced security + cross-model review.

## Architecture

```
OVERLAYS (always on, fire conditionally)
  • Risk Overlay  → auth/payments/AI/migrations → forced gates
  • AI Overlay    → LLM features → economics + safety + obs

P0 INTENT → P1 PLAN → P2 DESIGN → P3 BUILD → P4 VERIFY → P5 SHIP → P6 LEARN

INFRASTRUCTURE
  • 3-drawer memory (semantic / episodic / working STATE.md)
  • Evidence ledger (banned-phrase enforcement)
  • Deterministic router (auto-classifies work → suggests skill)
```

## The 23 skills

| Phase | Skills |
|---|---|
| **P0 Intent** | `/intent`, `/route` |
| **P1 Plan** | `/plan-ceo`, `/plan-eng`, `/plan-design` |
| **P2 Design** | `/design-shotgun`, `/design-build` |
| **P3 Build** | `/karpathy-check`, `/investigate`, `/review` |
| **P4 Verify** | `/qa`, `/cso`, `/codex`, `/evidence` |
| **P5 Ship** | `/risk-gate`, `/ship`, `/land-and-deploy`, `/canary` |
| **P6 Learn** | `/retro`, `/benchmark` |
| **AI Overlay** | `/ai-economics`, `/ai-safety`, `/ai-observability` |

## Install

```bash
./install.sh
```

## License

MIT — fork freely, contribute improvements back.

## Lineage

- gstack (Garry Tan) — roles, real-browser QA, deploy loop
- Dharma 0.x (Dilip Sahu) — evidence ledger, AI-native governance, 3-drawer memory
- Karpathy four failure modes — discipline gates
- Churney OS — Move Slow to Move Fast cadence
