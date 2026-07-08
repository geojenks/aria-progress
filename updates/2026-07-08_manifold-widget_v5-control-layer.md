---
area: manifold-widget
date: 2026-07-08
type: result
title: "unified_v5: control layer added, cross-language conformance closed"
---
The unified manifold↔MuJoCo tool reached v5, closing two gaps the earlier write-up
had flagged as open. First, cross-language conformance is now proven rather than
argued: golden vectors generated from the JavaScript kernel are reproduced exactly
by the Python kernel (a 24-case parity test, re-verified this week), so the widget a
person authors in and the model the physics runs are the same maths — the earlier
"verified by code review only" caveat no longer applies. Second, a real control layer
sits between manifold intent and enactment: a positional PI hold controller presses
the contact ring against the object's measured error, with a ~10 Hz feedback stream
carrying measured pose, tracking error and a loss-of-contact flag back to the author.
Re-verified this week (helpers off, natural grip): static hold 0.0 mm, hold-while-
spinning within 0.2 mm, and a 42 mm carry tracked within 0.1 mm. Grip force is
deliberately still outside the contract and is the next step.
