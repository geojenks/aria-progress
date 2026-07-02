---
area: manifold-planner
title: Manifold → MuJoCo live link
status: Stable
rag: g
take_home: A gait authored in dimensionless manifold coordinates streams over a websocket into a MuJoCo simulation that enacts it with a real hand model.
---
- The manifold prescribes *intent* (which regions contact, when, and the desired body motion); any manipulator that can enact that intent is a valid target.
- The execution side keeps the freedom the manifold does not specify: where to grip, how hard, IK feasibility.
- Next: the feedback channel reporting infeasible/unstable regions back to the manifold (Phase 4), and goal-led targets.
