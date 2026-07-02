---
area: manifold-widget
date: 2026-06-15
type: version
version: v12 (3-D)
title: 3-D widget renders the manipulated object
demo: demos/manifold-widget/v12/index.html
---
The authoring widget moved to 3-D with an upgrade that makes the manipulation legible:
it renders a spinning, semi-transparent "juggling ball" and shows the fingers dragging
it — previously the object was invisible and only the finger make/break pattern could
be seen. Every contacting node grips the same solid ball, so all contacts move together
at one shared speed. The widget is now embedded and interactive on this page (open the
demo, pick a preset, drag to orbit); the live 3-D physics link needs the local bridge,
so on this page the "Connect" button stays offline by design.
