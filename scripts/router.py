#!/usr/bin/env python3
"""
Dharma 1.0 — Deterministic Router

Classifies a task description and prints a Route Receipt:
  [Route X] Task: <summary>
  Start: /<skill>
  Overlays: [risk?, ai?]
  Forced gates: [...]

Usage:
  python3 scripts/router.py "fix login bug on safari"
  python3 scripts/router.py --task "build a billing dashboard"

The router is intentionally simple: keyword + regex rules.
No ML model. No hidden state. Easy to audit and tune.
"""

import argparse
import re
import sys
from typing import List, Tuple


# Risk overlay triggers — phrases or path-like tokens that imply high-risk surface.
RISK_TOKENS = [
    "auth", "login", "logout", "session", "oauth", "sso", "mfa", "2fa",
    "payment", "billing", "invoice", "subscription", "stripe", "paypal",
    "migration", "schema change", "alter table", "drop table",
    "prompt", "agent", "llm", "model", "rag",
    "policy", "permission", "rbac", "acl",
    "pii", "gdpr", "hipaa", "compliance",
]

# AI overlay triggers — phrases that imply LLM/AI features.
AI_TOKENS = [
    "llm", "prompt", "agent", "embedding", "rag", "vector",
    "openai", "anthropic", "claude", "gpt", "gemini",
    "chatbot", "summariz", "classif", "extract", "hallucinat",
    "ai feature", "ai-powered", "model selection",
]

# Bug fix language.
BUG_TOKENS = [
    "fix", "bug", "broken", "not working", "regression", "crash", "error",
    "exception", "fails to", "doesn't work", "issue with", "investigate",
]

# New product / 0→1.
PRODUCT_TOKENS = [
    "new product", "from scratch", "0 to 1", "mvp for", "build a new",
    "ground up", "greenfield",
]

# New feature.
FEATURE_TOKENS = [
    "add ", "implement", "new screen", "new page", "feature for",
    "ability to", "support for", "enable users to",
]

# UI/UX only.
DESIGN_TOKENS = [
    "redesign", "visual", "layout", "design system", "ui only",
    "ux only", "mockup", "wireframe",
]

# Refactor / behavior-preserving.
REFACTOR_TOKENS = [
    "refactor", "clean up", "rename", "restructure", "extract",
    "consolidate", "deduplicate",
]

# Performance.
PERF_TOKENS = [
    "slow", "performance", "optimize", "latency", "throughput",
    "memory leak", "bundle size",
]

# Security.
SECURITY_TOKENS = [
    "security", "vulnerability", "cve", "exploit", "harden",
    "owasp", "csrf", "xss", "injection",
]


def contains_any(text: str, tokens: List[str]) -> bool:
    """Case-insensitive substring match for any token."""
    lower = text.lower()
    return any(tok in lower for tok in tokens)


def classify(task: str) -> Tuple[str, str, List[str], List[str], List[str]]:
    """
    Returns (route, start_skill, overlays, forced_gates, exit_evidence).
    """
    overlays: List[str] = []
    forced_gates: List[str] = []

    # Step 1: risk surface check (overlay, not route decider).
    if contains_any(task, RISK_TOKENS):
        overlays.append("risk")
        forced_gates.extend(["cso", "codex", "qa"])

    # Step 2: AI feature check (overlay, not route decider).
    if contains_any(task, AI_TOKENS):
        overlays.append("ai")
        forced_gates.extend(["ai-economics", "ai-safety", "ai-observability"])

    # Step 3–7: route classification (first-match wins).
    if contains_any(task, BUG_TOKENS):
        route = "C — Bug Fix"
        start = "/investigate"
        exit_ev = ["Root cause documented", "Reproduction confirmed", "Fix tested"]
    elif contains_any(task, PRODUCT_TOKENS):
        route = "A — New Product"
        start = "/intent"
        exit_ev = ["PRD contract", "Scope decision logged", "Architecture diagram"]
    elif contains_any(task, DESIGN_TOKENS):
        route = "D — UI/UX"
        start = "/design-shotgun"
        exit_ev = ["Approved variant", "Production HTML", "QA visual pass"]
    elif contains_any(task, REFACTOR_TOKENS):
        route = "E — Refactor"
        start = "/karpathy-check"
        exit_ev = ["Zero behavior change", "Tests prove invariance", "Review clean"]
    elif contains_any(task, PERF_TOKENS):
        route = "F — Performance"
        start = "/benchmark"
        exit_ev = ["Baseline captured", "Improvement quantified", "No regression"]
    elif contains_any(task, SECURITY_TOKENS):
        route = "G — Security"
        start = "/cso"
        exit_ev = ["Findings triaged", "Fix with test", "Rollback plan"]
    elif contains_any(task, FEATURE_TOKENS):
        route = "B — New Feature"
        start = "/intent"
        exit_ev = ["PRD contract", "Plan complete", "Evidence ledger"]
    else:
        # Default fallback.
        route = "B — New Feature (default)"
        start = "/intent"
        exit_ev = ["PRD contract", "Plan complete", "Evidence ledger"]

    # Deduplicate forced gates while preserving order.
    seen = set()
    forced_gates = [g for g in forced_gates if not (g in seen or seen.add(g))]

    return route, start, overlays, forced_gates, exit_ev


def print_receipt(task: str) -> None:
    route, start, overlays, forced_gates, exit_ev = classify(task)
    overlays_str = ", ".join(overlays) if overlays else "none"
    gates_str = ", ".join(f"/{g}" for g in forced_gates) if forced_gates else "none"
    ev_str = "; ".join(exit_ev)

    print()
    print(f"[Route {route}]")
    print(f"  Task:                  {task}")
    print(f"  Start:                 {start}")
    print(f"  Overlays:              {overlays_str}")
    print(f"  Forced gates:          {gates_str}")
    print(f"  Exit evidence needed:  {ev_str}")
    print()


def main() -> int:
    parser = argparse.ArgumentParser(description="Dharma 1.0 router")
    parser.add_argument("task", nargs="*", help="task description")
    parser.add_argument("--task", dest="task_flag", help="task description (alt)")
    args = parser.parse_args()

    task = " ".join(args.task) if args.task else (args.task_flag or "")
    if not task.strip():
        print("Usage: router.py \"your task description\"", file=sys.stderr)
        return 2

    print_receipt(task.strip())
    return 0


if __name__ == "__main__":
    sys.exit(main())
