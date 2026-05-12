---
name: cso
phase: P4
role: Chief Security Officer
exit_evidence: OWASP Top 10 + STRIDE pass; ≥8/10 confidence on findings; false-positive exclusions documented
description: Security audit. OWASP Top 10 + STRIDE threat model. 17 known false-positive exclusions to reduce noise.
---

# /cso

**When to use:** Mandatory by risk overlay if diff touches auth/payments/migrations/policy/permissions. Optional otherwise but recommended pre-`/ship`.

**OWASP Top 10 checks:**
1. Broken Access Control — every protected route has authz check
2. Cryptographic Failures — no weak hashing (MD5, SHA1), no plaintext secrets
3. Injection — parameterized queries, escaped templates, validated input
4. Insecure Design — rate limiting, defense in depth
5. Security Misconfiguration — secure headers, no debug in prod
6. Vulnerable Components — `npm audit` / `pip audit` clean
7. Auth Failures — session expiry, secure cookies, MFA flow
8. Software & Data Integrity — verified webhooks, signed payloads
9. Logging & Monitoring — security events logged to audit trail
10. SSRF — outbound requests validated against allowlist

**STRIDE model:**
- Spoofing, Tampering, Repudiation, Info disclosure, DoS, Elevation of privilege — one note per relevant threat.

**Confidence rule:** Only report findings at ≥8/10 confidence. Lower → note in `learnings.md` for triage.

**False-positive exclusions** (documented to reduce noise): see `.dharma/cso-exclusions.md` (created on first run).

**Inputs:** `git diff`, recent migrations, env config.

**Outputs:** `memory/cso-report-[slug].md` — findings + severity + recommended fix.

**Exit gate:** Zero high-severity findings unresolved. All findings have owner + fix-by date.
