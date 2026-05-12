"""
Dharma 1.0 — AI Overlay CLI

Inspect telemetry, drift, and pricing without running any model.

Subcommands:
  pricing                List model pricing table
  suggest <bar>          Suggest cheapest model for a quality bar
  summary <path>         Read JSONL telemetry, print summary
  drift <path>           Run PSI drift detection on JSONL telemetry
  eval <eval-name>       Show eval set items (jailbreak / injection / hallucination / bias)
"""

import argparse
import json
import os
import sys
from pathlib import Path

# Support running as `python3 ai-runners/cli.py ...` from project root.
THIS = Path(__file__).resolve()
ROOT = THIS.parent.parent
sys.path.insert(0, str(ROOT))

# When run from `python3 -m ai-runners.cli`, relative imports work.
# When run directly, we need to import via absolute path.
try:
    from ai_runners.economics import PRICING, suggest_model
    from ai_runners.observability import Dashboard, DriftDetector
except ModuleNotFoundError:
    # Fallback: load by file (since "ai-runners" with a hyphen isn't importable directly).
    import importlib.util

    def _load(name: str, path: str):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    pkg = THIS.parent
    economics = _load("economics", str(pkg / "economics.py"))
    observability = _load("observability", str(pkg / "observability.py"))
    PRICING = economics.PRICING
    suggest_model = economics.suggest_model
    Dashboard = observability.Dashboard
    DriftDetector = observability.DriftDetector


def cmd_pricing(_args) -> int:
    print(json.dumps(PRICING, indent=2))
    return 0


def cmd_suggest(args) -> int:
    print(suggest_model(args.bar))
    return 0


def cmd_summary(args) -> int:
    path = args.path
    summary = Dashboard(path).summary()
    print(json.dumps(summary, indent=2))
    return 0


def cmd_drift(args) -> int:
    path = args.path
    detector = DriftDetector(path=path)
    report = detector.detect(baseline_n=args.baseline, current_n=args.current)
    print(json.dumps(report, indent=2))
    return 0


def cmd_eval(args) -> int:
    evals_dir = Path(args.evals_dir or (THIS.parent / "evals"))
    path = evals_dir / f"{args.name}.json"
    if not path.exists():
        print(f"no eval set named {args.name!r} at {path}", file=sys.stderr)
        return 1
    with open(path) as f:
        data = json.load(f)
    print(json.dumps(data, indent=2))
    return 0


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="ai-overlay", description="Dharma 1.0 AI Overlay CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    sp = sub.add_parser("pricing", help="list model pricing")
    sp.set_defaults(fn=cmd_pricing)

    sp = sub.add_parser("suggest", help="suggest model for quality bar")
    sp.add_argument("bar", choices=["cheap", "balanced", "best"])
    sp.set_defaults(fn=cmd_suggest)

    sp = sub.add_parser("summary", help="JSONL telemetry summary")
    sp.add_argument("path")
    sp.set_defaults(fn=cmd_summary)

    sp = sub.add_parser("drift", help="PSI drift detection")
    sp.add_argument("path")
    sp.add_argument("--baseline", type=int, default=100)
    sp.add_argument("--current", type=int, default=100)
    sp.set_defaults(fn=cmd_drift)

    sp = sub.add_parser("eval", help="print an eval set")
    sp.add_argument("name", choices=["jailbreak", "injection", "hallucination", "bias"])
    sp.add_argument("--evals-dir", default=None)
    sp.set_defaults(fn=cmd_eval)

    args = p.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
