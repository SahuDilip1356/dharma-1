"""
Dharma 1.0 — AI Economics

Tracks token usage and cost per LLM call. Enforces budget ceilings.
Provider-agnostic: caller passes input/output token counts; pricing table
maps model name → $/1M tokens.

Usage:
    tracker = TokenTracker(ceiling_usd=10.0)
    tracker.record(model="claude-sonnet-4-6", input_tokens=1200, output_tokens=340)
    if tracker.over_budget():
        raise BudgetExceeded(tracker.summary())
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional


# Pricing in USD per 1M tokens. Update as providers change.
# (input_price, output_price)
PRICING: Dict[str, Dict[str, float]] = {
    # Anthropic
    "claude-opus-4-7": {"input": 15.00, "output": 75.00},
    "claude-sonnet-4-6": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 0.80, "output": 4.00},
    # OpenAI
    "gpt-5": {"input": 10.00, "output": 30.00},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    # Google
    "gemini-2.0-pro": {"input": 2.50, "output": 10.00},
    "gemini-2.0-flash": {"input": 0.10, "output": 0.40},
}


class BudgetExceeded(Exception):
    """Raised when spend exceeds the hard ceiling."""


@dataclass
class Call:
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class TokenTracker:
    """Tracks LLM token usage and cost across a session."""

    ceiling_usd: float = 0.0
    alert_at: float = 0.80
    throttle_at: float = 1.00
    halt_at: float = 1.20
    calls: List[Call] = field(default_factory=list)

    def record(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        metadata: Optional[Dict[str, str]] = None,
    ) -> Call:
        """Record a single LLM call. Returns the Call object."""
        price = PRICING.get(model)
        if price is None:
            raise ValueError(
                f"Unknown model: {model!r}. Add to PRICING table in economics.py."
            )

        cost = (
            (input_tokens / 1_000_000) * price["input"]
            + (output_tokens / 1_000_000) * price["output"]
        )

        call = Call(
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost,
            metadata=metadata or {},
        )
        self.calls.append(call)

        if self.ceiling_usd > 0 and self.total_cost() >= self.ceiling_usd * self.halt_at:
            raise BudgetExceeded(
                f"Hard halt: spent ${self.total_cost():.4f} "
                f">= {self.halt_at * 100:.0f}% of ${self.ceiling_usd:.2f} ceiling"
            )

        return call

    def total_cost(self) -> float:
        return sum(c.cost_usd for c in self.calls)

    def total_input_tokens(self) -> int:
        return sum(c.input_tokens for c in self.calls)

    def total_output_tokens(self) -> int:
        return sum(c.output_tokens for c in self.calls)

    def budget_status(self) -> str:
        """Returns one of: ok | alert | throttle | halt | no-ceiling."""
        if self.ceiling_usd <= 0:
            return "no-ceiling"
        pct = self.total_cost() / self.ceiling_usd
        if pct >= self.halt_at:
            return "halt"
        if pct >= self.throttle_at:
            return "throttle"
        if pct >= self.alert_at:
            return "alert"
        return "ok"

    def over_budget(self) -> bool:
        return self.budget_status() in ("throttle", "halt")

    def summary(self) -> Dict[str, object]:
        """Return a dict summary suitable for JSON serialization."""
        return {
            "calls": len(self.calls),
            "total_input_tokens": self.total_input_tokens(),
            "total_output_tokens": self.total_output_tokens(),
            "total_cost_usd": round(self.total_cost(), 6),
            "ceiling_usd": self.ceiling_usd,
            "status": self.budget_status(),
            "by_model": self._by_model(),
        }

    def _by_model(self) -> Dict[str, Dict[str, float]]:
        out: Dict[str, Dict[str, float]] = {}
        for c in self.calls:
            row = out.setdefault(
                c.model, {"calls": 0, "input_tokens": 0, "output_tokens": 0, "cost_usd": 0.0}
            )
            row["calls"] += 1
            row["input_tokens"] += c.input_tokens
            row["output_tokens"] += c.output_tokens
            row["cost_usd"] += c.cost_usd
        for row in out.values():
            row["cost_usd"] = round(row["cost_usd"], 6)
        return out


def suggest_model(quality_bar: str = "balanced") -> str:
    """
    Cheapest model meeting a coarse quality bar.
    Quality bars: cheap | balanced | best
    """
    bars = {
        "cheap": "gemini-2.0-flash",
        "balanced": "claude-sonnet-4-6",
        "best": "claude-opus-4-7",
    }
    if quality_bar not in bars:
        raise ValueError(
            f"Unknown quality bar: {quality_bar!r}. Use one of: {list(bars)}"
        )
    return bars[quality_bar]
