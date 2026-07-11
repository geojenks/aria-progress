---
area: feature-space
date: 2026-07-10
type: version
version: v2
title: Records-driven actuator atlas — the interactive map is no longer a mock
demo: demos/actuator-map/v2/actuator_atlas.html
---
The interactive map has been rebuilt so that every number on the page is computed from
the measured actuator records (18 of them) rather than hand-placed for illustration —
the productionisation step promised when v1 shipped. It keeps the v1 interactions
(axis switching, actuation-level slider, per-actuator library cards, side-by-side
compare) and adds a deformation-composition view showing what fraction of each
actuator's motion is stretch vs bend vs twist, zoom and pan, a clickable actuator list
for picking any two to compare, and short replay animations of 13 of the actuators
embedded directly in their cards. The whole atlas is a single self-contained file that
works offline.
