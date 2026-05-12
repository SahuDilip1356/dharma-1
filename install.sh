#!/usr/bin/env bash
# Dharma 1.0 — 60-Second Installer
# Bootstraps Dharma into an existing repo: copies skills, installs git hooks,
# scaffolds memory drawers, verifies router.
#
# Usage:
#   ./install.sh                  # install into current repo
#   ./install.sh /path/to/repo    # install into target repo

set -euo pipefail

START_TIME=$(date +%s)

DHARMA_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET="${1:-$(pwd)}"

if [[ ! -d "${TARGET}" ]]; then
  echo "✗ target directory does not exist: ${TARGET}" >&2
  exit 1
fi

cd "${TARGET}"

echo "→ Installing Dharma 1.0 into: ${TARGET}"
echo ""

# Step 1: copy skills.
echo "  [1/6] copying skill catalog..."
mkdir -p .dharma/skills
cp -R "${DHARMA_ROOT}/skills/." .dharma/skills/
cp "${DHARMA_ROOT}/.dharma/config.yaml" .dharma/config.yaml
cp "${DHARMA_ROOT}/.dharma/routing-tree.md" .dharma/routing-tree.md

# Step 2: install hooks.
echo "  [2/6] installing git hooks..."
if [[ -d .git ]]; then
  mkdir -p .git/hooks
  cp "${DHARMA_ROOT}/hooks/evidence-ledger.sh" .git/hooks/commit-msg
  cp "${DHARMA_ROOT}/hooks/risk-overlay.sh" .git/hooks/pre-push
  chmod +x .git/hooks/commit-msg .git/hooks/pre-push
else
  echo "    (no .git/ directory — skipping hook install; run 'git init' first)"
fi

# Step 3: scaffold memory drawers if missing.
echo "  [3/6] scaffolding memory drawers..."
if [[ ! -d memory ]]; then
  cp -R "${DHARMA_ROOT}/memory/_template" memory
  echo "    created memory/ from template"
else
  for f in STATE.md semantic.md decisions.md learnings.md; do
    if [[ ! -f "memory/${f}" ]]; then
      cp "${DHARMA_ROOT}/memory/_template/${f}" "memory/${f}"
      echo "    added memory/${f}"
    fi
  done
  mkdir -p memory/episodic
fi

# Step 4: copy router script + AI runners.
echo "  [4/6] installing router + ai_runners..."
mkdir -p .dharma/scripts
cp "${DHARMA_ROOT}/scripts/router.py" .dharma/scripts/router.py
chmod +x .dharma/scripts/router.py
# AI runners — executable economics/safety/observability modules.
rm -rf .dharma/ai_runners
cp -R "${DHARMA_ROOT}/ai_runners" .dharma/ai_runners

# Step 5: write convenience CLI wrapper.
echo "  [5/6] writing CLI wrapper..."
cat > .dharma/dharma <<'EOF'
#!/usr/bin/env bash
# Dharma CLI — thin dispatcher.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CMD="${1:-help}"
shift || true
case "${CMD}" in
  route)   python3 "${ROOT}/scripts/router.py" "$@" ;;
  skills)  ls -1 "${ROOT}/skills"/*/*/SKILL.md | sed -E "s@.*/(.*)/SKILL.md@/\1@" | sort ;;
  config)  cat "${ROOT}/config.yaml" ;;
  ai)      PYTHONPATH="${ROOT}" python3 -m ai_runners.cli "$@" ;;
  help|*)  echo "dharma route <task> | dharma skills | dharma config | dharma ai <subcmd>" ;;
esac
EOF
chmod +x .dharma/dharma

# Step 6: verify.
echo "  [6/6] verifying install..."
SKILL_COUNT=$(find .dharma/skills -name SKILL.md | wc -l | tr -d ' ')
echo ""
if [[ "${SKILL_COUNT}" -eq 23 ]]; then
  echo "  ✓ ${SKILL_COUNT} skills installed"
else
  echo "  ⚠ expected 23 skills, found ${SKILL_COUNT}"
fi

if [[ -x .git/hooks/commit-msg ]]; then
  echo "  ✓ commit-msg hook active (evidence ledger)"
fi
if [[ -x .git/hooks/pre-push ]]; then
  echo "  ✓ pre-push hook active (risk overlay)"
fi
if [[ -x .dharma/scripts/router.py ]]; then
  echo "  ✓ router ready (.dharma/dharma route \"<task>\")"
fi
if [[ -d memory ]]; then
  echo "  ✓ memory drawers ready (memory/)"
fi

END_TIME=$(date +%s)
ELAPSED=$((END_TIME - START_TIME))

echo ""
echo "✓ Dharma 1.0 installed in ${ELAPSED}s"
echo ""
echo "Try it:"
echo "  .dharma/dharma route \"add a chatbot that answers FAQs\""
echo "  .dharma/dharma skills"
echo "  .dharma/dharma ai pricing"
echo "  .dharma/dharma ai suggest balanced"
echo ""
