// kernel.js — the normalized wave-manipulation model (single source of truth).
//
// Everything here lives in dimensionless "manifold space": the body is a unit
// sphere, time is seconds, and the one coordinate that crosses the seam to the
// 3D bridge is xi_norm in [0, 2pi). See ../core/schema.md.
//
// Schema @2 adds the full slice/superposition model:
//   - a bodyCircle manifold is a *slice* of the unit sphere: the great circle
//     perpendicular to `params.normal` (any direction, not just z).
//   - waves are `travelling` (the cup) or `standing` (the pinch). A standing
//     wave is implemented literally as the sum of two opposing travelling
//     waves:  [sin(k·dxi − φ) + sin(k·dxi + φ)]/2  =  sin(k·dxi)·cos(φ).
//   - each primitive carries a node `members` mask — which of the N ring nodes
//     it recruits (null = all).
//   - contact composes across primitives by AND (multiplicative contact,
//     additive lift), matching the validated sim hybrid; a node recruited by
//     no primitive is never in contact.
//
// Phase 1-2 scope grew into: bodyCircle slices in any orientation, travelling +
// standing waves, bodyRotation/translation flows, `free` lock.

export const SCHEMA = 'wave-manip/control-state@2';
const TWO_PI = Math.PI * 2;

// Contact tolerance: a node touches when W - T <= EPS. Mirrors the sim's
// `radial_disp <= 0.001 * r_amp` so a standing wave's envelope nodes (the
// pinch points, where W ~ 0 up to float noise) read as held, not flickering.
export const CONTACT_EPS = 1e-3;

// ── small vector helpers (exported for the widget's slice geometry) ──────────
export function normalize3(a) {
  const n = Math.hypot(a[0], a[1], a[2]) || 1;
  return [a[0] / n, a[1] / n, a[2] / n];
}
export function cross3(a, b) {
  return [a[1] * b[2] - a[2] * b[1], a[2] * b[0] - a[0] * b[2], a[0] * b[1] - a[1] * b[0]];
}

// Orthonormal frame (e1, e2, n) of a slice plane, n = the slice normal.
// Mirrors the sim's _build_rotation_frame so widget geometry matches the bridge.
export function planeBasis(axis) {
  const n = normalize3(axis);
  const up = Math.abs(n[0]) < 0.9 ? [1, 0, 0] : [0, 1, 0];
  const e1 = normalize3(cross3(n, up));
  const e2 = cross3(n, e1);
  return [e1, e2, n];
}

// Point on the slice's great circle (unit sphere) at manifold coordinate xi.
export function slicePoint(normal, xi) {
  const [e1, e2] = planeBasis(normal);
  const c = Math.cos(xi), s = Math.sin(xi);
  return [c * e1[0] + s * e2[0], c * e1[1] + s * e2[1], c * e1[2] + s * e2[2]];
}

// ── Manifold ────────────────────────────────────────────────────────────────
// The 1D curve the make/break wave lives on. `normUnit` is the arc length that
// maps to xi_norm = 2pi, so omega = 2pi*c*k/normUnit works across kinds.
// A bodyCircle is a *slice*: the great circle perpendicular to params.normal.
export function makeManifold(spec = { kind: 'bodyCircle' }) {
  const kind = spec.kind || 'bodyCircle';
  if (kind === 'worldLine') {
    return { kind, isClosed: false, normUnit: 1.0, params: { ...spec.params } };
  }
  if (kind === 'orbitCircle') {
    const R = spec.params?.R ?? 1.0;
    return { kind, isClosed: true, normUnit: TWO_PI * R, params: { R, ...spec.params } };
  }
  // bodyCircle (default): a great circle slice of the unit body sphere.
  const normal = normalize3(spec.params?.normal ?? [0, 0, 1]);
  return { kind: 'bodyCircle', isClosed: true, normUnit: TWO_PI, params: { normal } };
}

export const sliceNormal = (p) => p.manifold.params?.normal ?? [0, 0, 1];

// The axis through a standing wave's two envelope nodes (anchor and anchor+pi):
// the in-plane radial direction at xi = anchor. A `roll` flow — the pinch's
// perpendicular drive — rotates the body about this axis.
export function rollAxis(p) {
  return slicePoint(sliceNormal(p), p.wave.anchor);
}

// ── Flow: an SE(3) motion generator the body should follow ───────────────────
export function makeFlow(kind, overrides = {}) {
  const base = { kind, lock: 'free' };
  if (kind === 'bodyRotation') return { ...base, axis: [0, 0, 1], omega: 0, ...overrides };
  if (kind === 'translation') return { ...base, v: [0, 0, 0], ...overrides };
  if (kind === 'externalRotation') return { ...base, point: [0, 0, 0], axis: [0, 0, 1], omega: 0, ...overrides };
  return { ...base, ...overrides };
}

// ── Primitive: a make/break wave on a slice + flows + node membership ────────
export function makePrimitive(spec = {}) {
  return {
    name: spec.name || 'primitive',
    manifold: makeManifold(spec.manifold || { kind: 'bodyCircle' }),
    wave: {
      type: spec.wave?.type === 'standing' ? 'standing' : 'travelling',
      k: spec.wave?.k ?? 1,
      c: spec.wave?.c ?? 1.0,
      dc: spec.wave?.dc ?? 0.5,
      amp: spec.wave?.amp ?? 0.15,
      nWave: spec.wave?.nWave ?? 8,
      wavePhase: spec.wave?.wavePhase ?? 0, // authoring seed only
      anchor: spec.wave?.anchor ?? 0,       // standing-wave node position (xi)
    },
    flows: (spec.flows || []).map((f) => makeFlow(f.kind, f)),
    members: Array.isArray(spec.members) ? spec.members.map((i) => i | 0) : null,
    cLock: spec.cLock || 'free',
  };
}

export const isMember = (p, i) => p.members === null || p.members.includes(i);

// ── Wave math ────────────────────────────────────────────────────────────────
export const threshold = (p) => Math.sin(Math.PI * (p.wave.dc - 0.5));

// W(xi) at the primitive's CURRENT wavePhase. A standing wave is the sum of
// two opposing travelling waves (/2 keeps W in [-1, 1]):
//   [sin(k(xi−a) − φ) + sin(k(xi−a) + φ)] / 2  =  sin(k(xi−a))·cos(φ)
export function waveValue(p, xi) {
  const w = p.wave;
  if (w.type === 'standing') {
    const a = w.k * (xi - w.anchor);
    return 0.5 * (Math.sin(a - w.wavePhase) + Math.sin(a + w.wavePhase));
  }
  return Math.sin(w.k * xi - w.wavePhase);
}

// Effective phase speed after cLock resolution. Phase 1-2: only `free`.
export function waveC(p) {
  // world-frame / tracks-orbit locks need integrated body state — Phase 3.
  return p.wave.c;
}
export function waveOmega(p) {
  const nu = p.manifold.normUnit;
  return Math.abs(nu) < 1e-9 ? 0 : (TWO_PI * waveC(p) * p.wave.k) / nu;
}

// ── Body motion: SE(3) sum of all flows across all primitives ────────────────
export function bodyMotion(primitives, centroid = [0, 0, 0]) {
  const omega = [0, 0, 0];
  const v = [0, 0, 0];
  for (const p of primitives) {
    for (const f of p.flows) {
      if (f.kind === 'bodyRotation') {
        const a = normalize3(f.axis);
        omega[0] += f.omega * a[0];
        omega[1] += f.omega * a[1];
        omega[2] += f.omega * a[2];
      } else if (f.kind === 'translation') {
        v[0] += f.v[0]; v[1] += f.v[1]; v[2] += f.v[2];
      } else if (f.kind === 'externalRotation') {
        const a = normalize3(f.axis);
        const r = [centroid[0] - f.point[0], centroid[1] - f.point[1], centroid[2] - f.point[2]];
        // omega*axis x r
        v[0] += f.omega * (a[1] * r[2] - a[2] * r[1]);
        v[1] += f.omega * (a[2] * r[0] - a[0] * r[2]);
        v[2] += f.omega * (a[0] * r[1] - a[1] * r[0]);
      }
    }
  }
  return { omega_world: omega, v_world: v };
}

// ── The prescription: kernel output the bridge consumes each tick ────────────
// nNodes evenly spaced stations xi_i = i*2pi/N. Composition across primitives
// follows the validated sim hybrid: a node is in contact iff it is recruited
// by at least one primitive AND every recruiting primitive has wave(xi_i) <= its
// threshold (multiplicative contact); lifts add (additive lift).
//
// `t` is absolute seconds; with the `free` lock wavePhase(t) = seed + omega*t is
// exact, so prescribe() is pure (no integration state). Locks needing integrated
// body state arrive in Phase 3.
export function prescribe(controlState, nNodes, t) {
  const prims = (controlState.primitives || []).map(makePrimitive);
  const nodes = [];
  for (let i = 0; i < nNodes; i++) {
    const xi = (i / nNodes) * TWO_PI; // station on the unit ring
    let recruited = false;
    let contact = true;
    let lift = 0;
    for (const p of prims) {
      if (!isMember(p, i)) continue;
      recruited = true;
      const phased = { ...p, wave: { ...p.wave, wavePhase: p.wave.wavePhase + waveOmega(p) * t } };
      const W = waveValue(phased, xi);
      const T = threshold(p);
      if (W - T > CONTACT_EPS) {
        contact = false;
        lift += (W - T) * p.wave.amp;
      }
    }
    if (!recruited) contact = false;
    nodes.push({ i, contact, xi_norm: xi, lift });
  }
  return { t, nodes, body_motion: bodyMotion(prims) };
}

// Convenience for the widget preview: contact state for one primitive at xi.
export function nodeContact(primitive, xi, t) {
  const p = makePrimitive(primitive);
  const phased = { ...p, wave: { ...p.wave, wavePhase: p.wave.wavePhase + waveOmega(p) * t } };
  return waveValue(phased, xi) - threshold(p) <= CONTACT_EPS;
}
