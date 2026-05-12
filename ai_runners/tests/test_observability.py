"""Tests for ai_runners.observability."""

import json
import os
import tempfile
import unittest

from ai_runners.observability import (
    Dashboard,
    DriftDetector,
    TelemetryEmitter,
    psi,
)


class TestEmitter(unittest.TestCase):
    def test_emit_appends_jsonl(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            e = TelemetryEmitter(path)
            e.emit("claude-sonnet-4-6", 100, 50, 200, 0.001, refusal=False)
            e.emit("claude-sonnet-4-6", 200, 100, 350, 0.002, refusal=True)

            with open(path) as fh:
                lines = [json.loads(line) for line in fh if line.strip()]
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0]["model"], "claude-sonnet-4-6")
            self.assertEqual(lines[1]["refusal"], True)
        finally:
            os.unlink(path)


class TestDashboard(unittest.TestCase):
    def test_summary_empty(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            os.unlink(path)  # ensure file doesn't exist
            d = Dashboard(path)
            s = d.summary()
            self.assertEqual(s["count"], 0)
        except FileNotFoundError:
            pass

    def test_summary_aggregates(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            e = TelemetryEmitter(path)
            for i in range(10):
                e.emit("claude-sonnet-4-6", 100, 50, 100 + i * 10, 0.001, refusal=(i % 3 == 0))

            s = Dashboard(path).summary()
            self.assertEqual(s["count"], 10)
            self.assertGreater(s["latency_ms"]["p95"], s["latency_ms"]["p50"])
            self.assertAlmostEqual(s["cost_usd"]["total"], 0.01, places=4)
            # 4 of 10 should be refusals (i=0,3,6,9 → 4)
            self.assertEqual(s["refusal_rate"], 0.4)
            self.assertIn("claude-sonnet-4-6", s["by_model"])
        finally:
            os.unlink(path)


class TestPSI(unittest.TestCase):
    def test_identical_distributions_zero(self):
        d = [0.1, 0.2, 0.3, 0.2, 0.1, 0.05, 0.05, 0.0, 0.0, 0.0]
        self.assertAlmostEqual(psi(d, d), 0.0, places=3)

    def test_shifted_distribution_high(self):
        baseline = [0.5, 0.5, 0.0, 0.0, 0.0]
        current = [0.0, 0.0, 0.0, 0.5, 0.5]
        score = psi(baseline, current)
        self.assertGreater(score, 0.25)  # significant drift


class TestDriftDetector(unittest.TestCase):
    def test_insufficient_data(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            e = TelemetryEmitter(path)
            e.emit("claude-sonnet-4-6", 100, 50, 200, 0.001)
            d = DriftDetector(path)
            r = d.detect(baseline_n=10, current_n=10)
            self.assertEqual(r["status"], "insufficient-data")
        finally:
            os.unlink(path)

    def test_stable_when_no_change(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            e = TelemetryEmitter(path)
            for _ in range(40):
                e.emit("claude-sonnet-4-6", 100, 50, 200, 0.001)
            d = DriftDetector(path)
            r = d.detect(baseline_n=20, current_n=20)
            # Distribution identical → should be stable
            self.assertFalse(r["overall_drift"])
        finally:
            os.unlink(path)

    def test_drift_when_distribution_shifts(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            e = TelemetryEmitter(path)
            # Baseline: low latencies
            for _ in range(50):
                e.emit("claude-sonnet-4-6", 100, 50, 50, 0.001)
            # Current: much higher latencies
            for _ in range(50):
                e.emit("claude-sonnet-4-6", 100, 50, 5000, 0.001)
            d = DriftDetector(path)
            r = d.detect(baseline_n=50, current_n=50)
            self.assertTrue(r["overall_drift"])
            self.assertEqual(r["latency_ms"]["status"], "significant")
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()
