---
date: 2026-06-28
area: actuator-generators
milestone: WP3.1 / D3.1
agent: Claude (McKibben milestone session)
session_goal: Get the two-body McKibben generating true McKibben mechanics across braid angle
status: on-track
---

## What happened
- `workflow_2/make_mckibben.py` now produces a faithful two-body McKibben (soft bladder +
  helical braid as a separate contacting body + rigid end caps); contact wired in
  `parametricGripper.py`.
- Found the recipe that reproduces real mechanics: load-negligible bladder (braid carries
  hoop load), rigid caps, "fat" contact shell.
- Braid-angle sweep ×6 (20–70°) runs through the pipeline; added an angle-dependent
  line-line-contact toggle (high angles otherwise flood degenerate contacts).

## Progress vs the aim
- Gives D3.1 a genuine second, tunable actuator class: one design variable (braid helix
  angle) sweeps contract → neutral → extend across the ~54.7° magic angle. This is what
  a second class on the map needs.

## Ideas / decisions
- Braid angle is the right single axis to parameterise the class (clean qualitative flip).
- Rigid caps chosen over soft caps as the headline family (closer to real end fittings,
  holds contact better).

## Blockers / open questions
- None blocking. High-angle contact needed the toggle; documented in-file.

## Evidence
- `experiments/braid_angle/` sweep outputs; `magic_angle_flip.png` (kinematic flip).

## Next steps
- Run it through `jacobian.py` + `blocked_force_probe.py` and place on the cross-actuator map.
- Confirm the extend/contract polarity separates from the pneunets on the interpretable axes.
