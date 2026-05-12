"""
Dharma 1.0 — AI Overlay

Unified wrapper for any LLM callable. Wraps a model_fn so every call gets:
  • Token + cost tracking (economics)
  • Telemetry emission (observability)
  • Optional eval-on-deploy hook (safety)

Caller-provided token counter: a function (prompt, response) -> (in_tokens, out_tokens).
This keeps the overlay provider-agnostic; the caller knows how their provider
counts tokens.

Usage:
    from ai_runners.overlay import AIOverlay

    def my_model(prompt: str) -> str:
        # whatever provider call
        return "..."

    def count(prompt: str, response: str) -> tuple:
        return (len(prompt) // 4, len(response) // 4)  # rough fallback

    overlay = AIOverlay(
        model_fn=my_model,
        model_name="claude-sonnet-4-6",
        token_counter=count,
        telemetry_path="logs/llm.jsonl",
        ceiling_usd=10.0,
    )

    response = overlay("Summarize this document...")
    print(overlay.tracker.summary())
"""

import time
from dataclasses import dataclass, field
from typing import Callable, Dict, Optional, Tuple

from .economics import BudgetExceeded, TokenTracker
from .observability import TelemetryEmitter


TokenCounter = Callable[[str, str], Tuple[int, int]]


def default_token_counter(prompt: str, response: str) -> Tuple[int, int]:
    """Rough heuristic: 4 chars per token. Replace with real tokenizer in prod."""
    return (max(1, len(prompt) // 4), max(1, len(response) // 4))


@dataclass
class AIOverlay:
    """Provider-agnostic LLM wrapper with economics + observability."""

    model_fn: Callable[[str], str]
    model_name: str
    token_counter: TokenCounter = field(default=default_token_counter)
    telemetry_path: Optional[str] = "logs/llm.jsonl"
    ceiling_usd: float = 0.0
    refusal_keywords: Tuple[str, ...] = (
        "can't", "cannot", "won't", "decline", "refuse", "unable",
    )

    def __post_init__(self) -> None:
        self.tracker = TokenTracker(ceiling_usd=self.ceiling_usd)
        self.emitter: Optional[TelemetryEmitter] = (
            TelemetryEmitter(self.telemetry_path) if self.telemetry_path else None
        )

    def __call__(self, prompt: str, metadata: Optional[Dict[str, str]] = None) -> str:
        # Pre-flight: check budget before spending more.
        if self.tracker.over_budget():
            raise BudgetExceeded(
                f"budget already over (status={self.tracker.budget_status()}); "
                f"refusing to spend more"
            )

        start = time.time()
        response = self.model_fn(prompt)
        latency_ms = int((time.time() - start) * 1000)

        in_tok, out_tok = self.token_counter(prompt, response)
        call = self.tracker.record(
            model=self.model_name,
            input_tokens=in_tok,
            output_tokens=out_tok,
            metadata=metadata,
        )

        refusal = any(k in (response or "").lower() for k in self.refusal_keywords)

        if self.emitter is not None:
            self.emitter.emit(
                model=self.model_name,
                input_tokens=in_tok,
                output_tokens=out_tok,
                latency_ms=latency_ms,
                cost_usd=call.cost_usd,
                refusal=refusal,
                metadata=metadata,
            )

        return response

    def summary(self) -> Dict[str, object]:
        return self.tracker.summary()
