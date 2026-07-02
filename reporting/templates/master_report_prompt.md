# Master report — synthesis instruction

Give this to the master agent, with the reporting period, e.g.
"Synthesise the master report for Q1 (1 Apr – 30 Jun 2026)."

## Inputs (read in this order)
1. `PROJECT_AIMS.md` — the yardstick. Every claim maps to an aim/milestone here.
2. `weekly/` files whose `week` falls in the period — the primary source.
3. `sessions/` files — only when a weekly rollup is thin and you need the detail.

## What to produce
A **plan-level report first** (the skim layer), expandable on request. Match the house
style already in `ARIA reports/July/ARIA_Q1_2026_AT_A_GLANCE_GJ.md`:
- Per-area blocks, not wide tables (George reads raw markdown).
- Each block: what it is / why it matters, then `Apr → Jul → Next` (or the period's
  start → end → next).
- A HEADLINE block: milestone, status, what "concluded" needs, team changes, RAG.
- A NEXT-period critical path.

## Rules of synthesis
- **Map everything to `PROJECT_AIMS.md`.** Group by milestone; an entry with no aim is a
  flag, not a section.
- **Roll up `status`/`rag`**: any `red` in a milestone → surface it; `blocked` → into
  risks. Don't average away a problem.
- **Report faithfully.** "In progress" ≠ "done". If evidence is missing, say so.
- **No editorialising about other teams' pace.** State what was used/built; don't frame
  upstream delays as complaints (per George's standing preference).
- **Prefer the precise remaining-work statement** over an overclaim — "here's what
  concludes it" reads better than "essentially done".
- Pull `Evidence` items forward as the artefact list for the portal.

## Output
Write to `reports/<period>.md`. Note any `‹↻›` gaps where an area's rollup was missing,
so George knows what to chase before submission.
