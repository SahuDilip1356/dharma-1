"""Tests for ai_runners.economics."""

import unittest

from ai_runners.economics import (
    BudgetExceeded,
    PRICING,
    TokenTracker,
    suggest_model,
)


class TestPricing(unittest.TestCase):
    def test_known_models_have_pricing(self):
        for m in ["claude-sonnet-4-6", "gpt-4o", "gemini-2.0-flash"]:
            self.assertIn(m, PRICING)
            self.assertIn("input", PRICING[m])
            self.assertIn("output", PRICING[m])


class TestSuggestModel(unittest.TestCase):
    def test_balanced_returns_sonnet(self):
        self.assertEqual(suggest_model("balanced"), "claude-sonnet-4-6")

    def test_cheap_returns_flash(self):
        self.assertEqual(suggest_model("cheap"), "gemini-2.0-flash")

    def test_best_returns_opus(self):
        self.assertEqual(suggest_model("best"), "claude-opus-4-7")

    def test_unknown_bar_raises(self):
        with self.assertRaises(ValueError):
            suggest_model("godmode")


class TestTokenTracker(unittest.TestCase):
    def test_record_computes_cost(self):
        t = TokenTracker()
        # Sonnet: $3/1M input, $15/1M output
        # 1000 input + 200 output = 0.003 + 0.003 = 0.006
        t.record("claude-sonnet-4-6", input_tokens=1000, output_tokens=200)
        self.assertAlmostEqual(t.total_cost(), 0.006, places=6)

    def test_unknown_model_raises(self):
        t = TokenTracker()
        with self.assertRaises(ValueError):
            t.record("nonexistent-model", 100, 100)

    def test_budget_status_thresholds(self):
        # Use cheap model: gemini-flash $0.10 / 1M input
        # 100M input tokens = $10 ceiling test
        t = TokenTracker(ceiling_usd=1.0)
        self.assertEqual(t.budget_status(), "ok")

        # Get to 80%: $0.80. At $0.10/1M input, that's 8M tokens.
        t.record("gemini-2.0-flash", input_tokens=8_000_000, output_tokens=0)
        self.assertEqual(t.budget_status(), "alert")

        # Get to 100%: another $0.20 = 2M more tokens.
        t.record("gemini-2.0-flash", input_tokens=2_000_000, output_tokens=0)
        self.assertEqual(t.budget_status(), "throttle")

    def test_halt_raises(self):
        t = TokenTracker(ceiling_usd=0.01)  # very low ceiling
        with self.assertRaises(BudgetExceeded):
            # one big call blows the ceiling
            t.record("claude-opus-4-7", input_tokens=10_000_000, output_tokens=10_000_000)

    def test_summary_shape(self):
        t = TokenTracker(ceiling_usd=5.0)
        t.record("claude-sonnet-4-6", 1000, 500)
        t.record("gpt-4o-mini", 2000, 1000)
        s = t.summary()
        self.assertEqual(s["calls"], 2)
        self.assertEqual(s["total_input_tokens"], 3000)
        self.assertEqual(s["total_output_tokens"], 1500)
        self.assertIn("by_model", s)
        self.assertEqual(set(s["by_model"].keys()), {"claude-sonnet-4-6", "gpt-4o-mini"})
        self.assertEqual(s["status"], "ok")

    def test_no_ceiling_status(self):
        t = TokenTracker()  # ceiling_usd=0
        t.record("claude-sonnet-4-6", 1000, 100)
        self.assertEqual(t.budget_status(), "no-ceiling")
        self.assertFalse(t.over_budget())


if __name__ == "__main__":
    unittest.main()
