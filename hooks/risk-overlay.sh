#!/usr/bin/env bash
# Dharma 1.0 — Risk Overlay Hook
# Pre-push check. Blocks if diff touches high-risk paths and required gate receipts are missing.
# Install as: .git/hooks/pre-push

set -euo pipefail

REMOTE="${1:-origin}"
URL="${2:-}"

# Determine base branch (best-effort).
BASE_BRANCH="$(git symbolic-ref refs/remotes/${REMOTE}/HEAD 2>/dev/null | sed "s@^refs/remotes/${REMOTE}/@@" || echo "main")"

# Find merge base with base branch.
MERGE_BASE="$(git merge-base HEAD "${REMOTE}/${BASE_BRANCH}" 2>/dev/null || git rev-parse HEAD~1)"

# Get list of changed files.
CHANGED="$(git diff --name-only "${MERGE_BASE}"...HEAD || true)"

if [[ -z "${CHANGED}" ]]; then
  exit 0
fi

# Risk patterns — regex, OR-joined.
RISK_REGEX='(^|/)(auth|payments|billing|migrations|prompts|llm|agents|permissions)(/|$)|\.sql$|\.policy\.'

RISKY_FILES="$(echo "${CHANGED}" | grep -E "${RISK_REGEX}" || true)"

if [[ -z "${RISKY_FILES}" ]]; then
  echo "risk-overlay: no high-risk paths touched. proceeding."
  exit 0
fi

echo ""
echo "⚠ risk-overlay: high-risk paths detected:"
echo "${RISKY_FILES}" | sed 's/^/  - /'
echo ""
echo "Required gate receipts (in memory/ from this branch, last 24h):"

# Check for required receipts.
MISSING=()
for gate in cso codex qa; do
  # Look for any recent receipt matching gate name.
  RECEIPT="$(find memory -maxdepth 2 -name "${gate}*.md" -mtime -1 2>/dev/null | head -1 || true)"
  if [[ -z "${RECEIPT}" ]]; then
    MISSING+=("/${gate}")
    echo "  ✗ /${gate} — missing"
  else
    echo "  ✓ /${gate} — ${RECEIPT}"
  fi
done

if [[ "${#MISSING[@]}" -gt 0 ]]; then
  echo ""
  echo "BLOCKED: run the missing gates before pushing:" >&2
  for g in "${MISSING[@]}"; do
    echo "  ${g}" >&2
  done
  echo ""
  echo "To bypass (logged to memory/learnings.md):" >&2
  echo "  DHARMA_RISK_BYPASS=\"<justification>\" git push" >&2
  echo ""

  if [[ -n "${DHARMA_RISK_BYPASS:-}" ]]; then
    mkdir -p memory
    echo "## $(date -u +%Y-%m-%dT%H:%M:%SZ) — risk-overlay bypass" >> memory/learnings.md
    echo "**Files:** ${RISKY_FILES//$'\n'/, }" >> memory/learnings.md
    echo "**Missing gates:** ${MISSING[*]}" >> memory/learnings.md
    echo "**Justification:** ${DHARMA_RISK_BYPASS}" >> memory/learnings.md
    echo "" >> memory/learnings.md
    echo "risk-overlay: bypass logged. proceeding." >&2
    exit 0
  fi

  exit 1
fi

echo ""
echo "✓ risk-overlay: all required gates have fresh receipts. proceeding."
exit 0
