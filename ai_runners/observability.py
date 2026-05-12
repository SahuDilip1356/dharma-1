"""
Dharma 1.0 — AI Observability

Structured logging + drift detection for LLM calls.

Emits one JSONL line per call. Reads them back for dashboard summaries
and drift detection on token / latency distributions.

Drift uses Population Stability Index (PSI), a stdlib-only proxy for
KL divergence on binned distributions. PSI > 0.25 = significant drift.

Usage:
    emitter = TelemetryEmitter("logs/llm.jsonl")
    emitter.emit(
        model="claude-sonnet-4-6",
        input_tokens=1200,
        output_tokens=340,
        latency_ms=850,
        cost_usd=0.0087,
    )

    summary = Dashboard("logs/llm.jsonl").summary()
"""

import json
import math
import os
import statistics
import time
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional


@dataclass
class CallRecord:
    """One structured log line."""

    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    latency_ms: int
    cost_usd: float
    refusal: bool = False
    eval_score: Optional[float] = None
    request_id: Optional[str] = None
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass
class TelemetryEmitter:
    """Append-only JSONL emitter."""

    path: str

    def __post_init__(self) -> None:
        Path(self.path).parent.mkdir(parents=True, exist_ok=True)

    def emit(
        self,
        model: str,
        input_tokens: int,
        output_tokens: int,
        latency_ms: int,
        cost_usd: float,
        refusal: bool = False,
        eval_score: Optional[float] = None,
        request_id: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None,
    ) -> CallRecord:
        rec = CallRecord(
            timestamp=time.time(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            latency_ms=latency_ms,
            cost_usd=cost_usd,
            refusal=refusal,
            eval_score=eval_score,
            request_id=request_id,
            metadata=metadata or {},
        )
        with open(self.path, "a") as f:
            f.write(json.dumps(asdict(rec)) + "\n")
        return rec


def _percentile(values: List[float], p: float) -> float:
    """Linear-interpolation percentile. p in [0, 100]."""
    if not values:
        return 0.0
    s = sorted(values)
    k = (len(s) - 1) * (p / 100.0)
    f = math.floor(k)
    c = math.ceil(k)
    if f == c:
        return s[int(k)]
    return s[f] * (c - k) + s[c] * (k - f)


def _read_jsonl(path: str) -> List[dict]:
    if not os.path.exists(path):
        return []
    out: List[dict] = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                out.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return out


@dataclass
class Dashboard:
    """Read JSONL telemetry and produce summary metrics."""

    path: str

    def records(self) -> List[dict]:
        return _read_jsonl(self.path)

    def summary(self) -> Dict[str, object]:
        recs = self.records()
        if not recs:
            return {"count": 0, "note": "no telemetry yet"}

        latencies = [r["latency_ms"] for r in recs if "latency_ms" in r]
        costs = [r["cost_usd"] for r in recs if "cost_usd" in r]
        refusals = sum(1 for r in recs if r.get("refusal"))
        by_model = Counter(r["model"] for r in recs if "model" in r)

        return {
            "count": len(recs),
            "latency_ms": {
                "p50": round(_percentile(latencies, 50), 1),
                "p95": round(_percentile(latencies, 95), 1),
                "p99": round(_percentile(latencies, 99), 1),
                "mean": round(statistics.fmean(latencies), 1) if latencies else 0,
            },
            "cost_usd": {
                "total": round(sum(costs), 6),
                "mean_per_call": round(sum(costs) / len(costs), 6) if costs else 0,
            },
            "refusal_rate": round(refusals / len(recs), 4) if recs else 0.0,
            "by_model": dict(by_model),
        }


# --- Drift detection ---------------------------------------------------------


def _histogram(
    values: Iterable[float],
    bins: int = 10,
    bin_range: Optional[tuple] = None,
) -> List[float]:
    """
    Return normalized histogram (fractions summing to 1).

    If `bin_range` is supplied, use it as (lo, hi) — required for comparing
    two distributions on shared bins. Otherwise, infer from values.
    """
    vs = list(values)
    if not vs:
        return [0.0] * bins

    if bin_range is not None:
        lo, hi = bin_range
    else:
        lo, hi = min(vs), max(vs)

    if hi == lo:
        out = [0.0] * bins
        out[0] = 1.0
        return out

    width = (hi - lo) / bins
    counts = [0] * bins
    for v in vs:
        if v <= lo:
            idx = 0
        elif v >= hi:
            idx = bins - 1
        else:
            idx = min(bins - 1, int((v - lo) / width))
        counts[idx] += 1
    total = sum(counts)
    return [c / total for c in counts] if total else [0.0] * bins


def psi(baseline: List[float], current: List[float]) -> float:
    """
    Population Stability Index.
    <0.10 = stable, 0.10–0.25 = moderate drift, >0.25 = significant drift.
    """
    if len(baseline) != len(current):
        raise ValueError("baseline and current must have same number of bins")
    eps = 1e-6
    total = 0.0
    for b, c in zip(baseline, current):
        b = max(b, eps)
        c = max(c, eps)
        total += (c - b) * math.log(c / b)
    return total


@dataclass
class DriftDetector:
    """Compares a baseline window vs a current window of telemetry."""

    path: str
    bins: int = 10
    significant_threshold: float = 0.25

    def detect(self, baseline_n: int = 100, current_n: int = 100) -> Dict[str, object]:
        recs = _read_jsonl(self.path)
        if len(recs) < baseline_n + current_n:
            return {
                "status": "insufficient-data",
                "needed": baseline_n + current_n,
                "have": len(recs),
            }

        baseline = recs[-baseline_n - current_n : -current_n]
        current = recs[-current_n:]

        report: Dict[str, object] = {}
        for field_name in ("input_tokens", "latency_ms"):
            b_vals = [r[field_name] for r in baseline if field_name in r]
            c_vals = [r[field_name] for r in current if field_name in r]
            # Shared binning so the two histograms are comparable.
            combined = b_vals + c_vals
            if combined:
                bin_range = (min(combined), max(combined))
            else:
                bin_range = (0.0, 1.0)
            b_hist = _histogram(b_vals, self.bins, bin_range=bin_range)
            c_hist = _histogram(c_vals, self.bins, bin_range=bin_range)
            score = psi(b_hist, c_hist)
            status = (
                "stable" if score < 0.10
                else "moderate" if score < self.significant_threshold
                else "significant"
            )
            report[field_name] = {"psi": round(score, 4), "status": status}

        report["overall_drift"] = any(
            v["status"] == "significant"
            for v in report.values()
            if isinstance(v, dict) and "status" in v
        )
        return report
