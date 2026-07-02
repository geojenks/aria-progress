# Project Aims — the yardstick
*(WP3 subsection George Jenkinson owns, within the ARIA dexterous soft-robotics
programme. Every report maps onto the deliverables/milestones and area slugs below.
Verified against "ARIA full proposal with Revised Scopes Final.pdf", 2026-07-02.)*

Programme: ARIA Robot Dexterity · PI Dr Min Pan (University of Bath).
WP3 ("Creation of an analytical modelling framework … dexterous soft robotic
manipulators") runs Months 12–36.

---

## Deliverables & milestones George reports against (from the proposal)

- **D3.1 — Characteristics classification methodology (WP3.1). Month 28. *Primary.***
  Proposal spec: clustered points in a finite-dimensional feature space reflecting
  underlying common characteristics; features such as linear, rotating, bending,
  twisting motion, flexibility, load capacity, actuation speed, material stiffness;
  clustering with a similarity/distance measure. *New scope:* collaborate with
  Co-designer Cambridge (sim-to-real / real-to-sim), Months 15–23.
- **D3.2 — Model dimensionality reduction methodology (WP3.2). Month 30.**
  Low-dimensional subspace capture, multidimensional scaling, local embeddings on
  low-dimensional manifolds. *Revised-scope note:* may be less comprehensive than
  originally proposed (reduced RA3 timeframe); functional deliverable still expected.
  George's wave-based manipulation thread (intent-vs-execution manifold split) reports
  its WP3.2 relevance here.
- **D3.3 — Validated analytical framework + benchmark (WP3.3). Month 34.**
- **D3.4 — Optimised soft manipulator case study (WP3.4). Month 36.**
  WP3.4 evaluates the framework with the **EARCTV** metrics (Effectiveness, Accuracy,
  Robustness, Computation requirement, Transformability, Versatility). *New scope:*
  Co-designer MorphoAI on simulation algorithms, Months 25–27.

Proposal-numbered milestones: M1 validated high-fidelity modelling tool (M23);
M2 validated PIML models (M24); M3 validated analytical framework + benchmark (M34);
M4 optimised-manipulator case study (M36).

**Portal milestone numbering differs from the proposal's M1–M4.** In the ARIA portal
scheme the project reports against more milestones; the one George's manipulation
thread connects to is **Milestone 5 — "Mathematical models for internal physical
interactions of the soft manipulators"** (the proposal's D1.3 theme; PI suggested the
connection). The April report and the "M-05 - Internal physical interactions Results -
Jan 2026" submission both reference it — the wave framework expands its
geometric-factors theme (how contact geometry determines the interaction).

---

## Areas (the `area` slugs used in front-matter)

Each area is owned by a work agent; it maps to exactly one deliverable.

| area slug | maps to | one-line scope |
|---|---|---|
| `classification-pipeline` | D3.1 | end-to-end methodology → running pipeline |
| `actuator-generators` | D3.1 | parametric CAD/mesh generators (portable tooling) |
| `mesh-labelling-gui` | D3.1 | GUI to label meshes into the pipeline |
| `classification-data` | D3.1 | simulated + literature experiments / evidence |
| `feature-space` | D3.1 | feature space, distance metric, actuator map |
| `wave-theory` | D3.2 (WP3.2) | gait theory + superposition |
| `manifold-widget` | D3.2 (WP3.2) | 2D/3D manifold authoring widget |
| `manipulator-ik` | D3.2 (WP3.2) / portal M5 | wave → arbitrary actuator via IK |
| `manifold-planner` | D3.2 (WP3.2) | plan in manifold space → export to MuJoCo |
| `software-library` | (cross-cutting) | the gated repo / reusable outputs register |

*(This table is the reconciliation key: a session/weekly file whose `area` isn't here
should be caught and fixed, not silently reported.)*
