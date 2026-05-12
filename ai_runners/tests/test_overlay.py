"""Tests for ai_runners.overlay."""

import json
import os
import tempfile
import unittest

from ai_runners.economics import BudgetExceeded
from ai_runners.overlay import AIOverlay, default_token_counter


def echo_model(prompt: str) -> str:
    return f"Got: {prompt[:50]}"


def refuser_model(_prompt: str) -> str:
    return "I can't help with that request."


class TestDefaultCounter(unittest.TestCase):
    def test_counter_returns_positive(self):
        a, b = default_token_counter("hello world", "response text here")
        self.assertGreater(a, 0)
        self.assertGreater(b, 0)


class TestOverlay(unittest.TestCase):
    def test_basic_call_records(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            overlay = AIOverlay(
                model_fn=echo_model,
                model_name="claude-sonnet-4-6",
                telemetry_path=path,
                ceiling_usd=1.0,
            )
            r1 = overlay("first prompt")
            r2 = overlay("second prompt")

            self.assertTrue(r1.startswith("Got:"))
            self.assertTrue(r2.startswith("Got:"))

            # Tracker should have 2 calls
            self.assertEqual(len(overlay.tracker.calls), 2)

            # JSONL should have 2 lines
            with open(path) as fh:
                lines = [json.loads(line) for line in fh if line.strip()]
            self.assertEqual(len(lines), 2)
            self.assertFalse(lines[0]["refusal"])
        finally:
            os.unlink(path)

    def test_refusal_detected(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            overlay = AIOverlay(
                model_fn=refuser_model,
                model_name="claude-sonnet-4-6",
                telemetry_path=path,
                ceiling_usd=1.0,
            )
            overlay("anything")

            with open(path) as fh:
                line = json.loads(fh.readline())
            self.assertTrue(line["refusal"])
        finally:
            os.unlink(path)

    def test_budget_blocks_further_calls(self):
        with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            path = f.name
        try:
            # Tiny ceiling — first big call should consume it.
            overlay = AIOverlay(
                model_fn=lambda p: "x" * 100_000,  # big response
                model_name="claude-opus-4-7",
                telemetry_path=path,
                ceiling_usd=0.0001,
            )
            # First call may raise BudgetExceeded during record (post-halt-check),
            # OR the second call's pre-flight should refuse.
            with self.assertRaises(BudgetExceeded):
                overlay("a" * 100_000)
                overlay("a" * 100_000)
        finally:
            os.unlink(path)

    def test_no_telemetry_path(self):
        overlay = AIOverlay(
            model_fn=echo_model,
            model_name="claude-sonnet-4-6",
            telemetry_path=None,
            ceiling_usd=1.0,
        )
        r = overlay("test")
        self.assertTrue(r.startswith("Got:"))
        self.assertEqual(len(overlay.tracker.calls), 1)


if __name__ == "__main__":
    unittest.main()
