#!/usr/bin/env bash
# Dharma 1.0 — Evidence Ledger Hook
# Enforces completion language at commit time.
# Install as: .git/hooks/commit-msg (symlink or copy)
#
# Rejects commits whose message contains banned phrases.
# Requires the message to contain a valid completion-state phrase.

set -euo pipefail

MSG_FILE="${1:-}"
if [[ -z "${MSG_FILE}" || ! -f "${MSG_FILE}" ]]; then
  echo "evidence-ledger: no commit message file passed; skipping." >&2
  exit 0
fi

MSG="$(cat "${MSG_FILE}")"

# Banned phrases — case-insensitive substring match.
BANNED=(
  "should work"
  "should be fine"
  "should pass"
  "probably works"
  "probably passes"
  "i believe it's fixed"
  "i believe its fixed"
  "looks correct"
  "seems to work"
  "appears correct"
)

LOWER="$(echo "${MSG}" | tr '[:upper:]' '[:lower:]')"

for phrase in "${BANNED[@]}"; do
  if echo "${LOWER}" | grep -qF "${phrase}"; then
    echo "" >&2
    echo "✗ evidence-ledger: commit message contains banned phrase: \"${phrase}\"" >&2
    echo "" >&2
    echo "  Use one of the 5 valid completion states instead:" >&2
    echo "    1. Implemented and verified with [evidence]." >&2
    echo "    2. Implemented but not runtime-verified — [what's missing]." >&2
    echo "    3. Planned only; no code changed." >&2
    echo "    4. Partially complete; remaining risks: [list]." >&2
    echo "    5. Blocked: [specific blocker]." >&2
    echo "" >&2
    exit 1
  fi
done

# Soft check: encourage at least one valid state phrase for non-trivial commits.
# Counts non-comment lines > 1 as "non-trivial".
NON_COMMENT_LINES=$(echo "${MSG}" | grep -vc '^#' || true)
if [[ "${NON_COMMENT_LINES}" -gt 1 ]]; then
  VALID_FOUND=0
  for valid in "implemented and verified" "implemented but not runtime-verified" "planned only" "partially complete" "blocked:"; do
    if echo "${LOWER}" | grep -qF "${valid}"; then
      VALID_FOUND=1
      break
    fi
  done
  if [[ "${VALID_FOUND}" -eq 0 ]]; then
    echo "⚠ evidence-ledger: commit doesn't reference a completion state." >&2
    echo "  Consider adding one of: implemented and verified | implemented but not runtime-verified |" >&2
    echo "  planned only | partially complete | blocked." >&2
    echo "  (Warning only — commit allowed.)" >&2
  fi
fi

exit 0
