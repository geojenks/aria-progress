---
area: manifold-widget
title: Manifold authoring widget (2-D / 3-D)
status: 2-D & 3-D live on page
rag: g
take_home: Author a manipulation in a low-dimensional "manifold" (intent) space — both the 2-D and 3-D widgets now run interactively on this page, the 3-D one rendering the manipulated object being dragged by the fingers.
---
- The 2-D widget remains the clean conceptual basis; the manipulations grew complex enough that they needed 3-D.
- The 3-D preview draws a spinning "juggling ball": every contacting node grips the same solid ball, so all contacts move together at one shared speed.
- Both widgets are self-contained static pages served from this site; the 3-D one's live physics link (to the MuJoCo bridge) runs locally, so on the hosted page "Connect" stays offline by design.
