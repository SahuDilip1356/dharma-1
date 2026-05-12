---
name: design-shotgun
phase: P2
role: Design Explorer
exit_evidence: 4–6 variants generated; one approved; taste log updated
description: Generate 4–6 design variants for the same screen. Compare side-by-side. Learn taste over time.
---

# /design-shotgun

**When to use:** Route D (UI/UX-first) or Route B with significant UX surface. Especially valuable when "I'm not sure what this should look like."

**Process:**
1. Read approved direction from `/plan-design`.
2. Generate 4–6 variants varying along ONE axis at a time (layout / type scale / color / density).
3. Render as static HTML mockups side-by-side.
4. User picks one (or hybrid). Choice + reasoning written to `memory/taste.md`.
5. Taste log decays 5%/week — fresh preferences outweigh stale ones in future runs.

**Variant axes (rotate per session):**
- Layout: sidebar vs. topnav vs. tabs vs. command-palette
- Type: tight vs. loose, serif vs. sans
- Color: neutral-led vs. accent-led vs. monochrome
- Density: information-dense vs. whitespace-led

**Inputs:** Direction from `/plan-design`, content/copy from `/intent`.

**Outputs:**
- `design-shotgun/[slug]/v1.html`...`v6.html`
- `design-shotgun/[slug]/compare.html` — side-by-side board
- `memory/taste.md` — chosen variant + reasoning

**Exit gate:** One variant approved. Reasoning ≥2 sentences logged.
