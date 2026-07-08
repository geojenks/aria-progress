---
area: manifold-widget
title: Manifold authoring widget (2-D / 3-D)
status: 2-D & 3-D live on page; v5 control layer
rag: g
take_home: Author a manipulation in a low-dimensional "manifold" (intent) space — both widgets run interactively here; the tool (v5) now proves the JS↔Python kernels identical (golden-vector parity) and adds a positional hold controller with a live feedback stream, so authored intent is enacted and tracked, not just previewed.
---
- The 2-D widget remains the clean conceptual basis; the manipulations grew complex enough that they needed 3-D.
- The 3-D preview draws a spinning "juggling ball": every contacting node grips the same solid ball, so all contacts move together at one shared speed.
- Both widgets are self-contained static pages served from this site; the 3-D one's live physics link (to the MuJoCo bridge) runs locally, so on the hosted page "Connect" stays offline by design.
