---
area: feature-space
title: Feature space & actuator map
status: Core D3.1 criterion met in simulation
rag: g
take_home: Distinct simulated actuator classes separate cleanly on interpretable, named axes — the D3.1 outcome, in simulation — and the map now answers design questions both ways, grading the library against a requirement and steering the design of a new actuator whose predicted behaviour was then confirmed.
---
- **Interpretable, named axes** (axial / bend / twist / stroke-authority / blocked-force) — matching the feature set the proposal anticipates for WP3.1.
- **Actuators are trajectories, not points:** design families draw as ribbons, multi-input devices as reachable hulls — class boundaries stay emergent, not imposed.
- **An interactive atlas driven by the measured records** (no hand-placed numbers): switch axes, scrub actuation, zoom/pan, open per-actuator library cards with replay animations, pick any two actuators to compare side by side.
- **A validated design prediction:** a slack-tendon bellows designed from the map's coordinates changes behaviour type mid-stroke as predicted — and is invisible to a classical force–stroke chart, which the deformation axes resolve.
- **Requirement-driven selection:** an illustrative spec shaded onto the Ashby-style chart plus a traceable pass/fail matrix picks the bellows as the sole outright pass; the contracting McKibbens verify as a common iso-energy contour (F·x ≈ 3.3 mJ).
