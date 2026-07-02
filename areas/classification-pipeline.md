---
area: classification-pipeline
title: Analysis pipeline
status: Stable — running end-to-end
rag: g
take_home: A soft-actuator design goes in; a controllability/observability fingerprint and a place on the cross-actuator map come out — end-to-end on FEM (SOFA) and literature data.
note: Simulated absolutes are comparative (not predictive) pending calibration against empirical data; extending the blocked-force measure to bending actuators (net moment) is in progress as part of the hardening work.
---
- **Actuator-agnostic chain:** labelled mesh → SOFA pressure sweep → per-actuator Gramian fingerprint → blocked-force sweep → cross-actuator map.
- **Source-agnostic:** the same pipeline ingests simulation, experiment, or literature data unchanged.
- **Divergence-safe sweeps** settle each pressure level to a kinetic-energy threshold and stop cleanly at the stability limit.
