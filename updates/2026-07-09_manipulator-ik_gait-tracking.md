---
area: manipulator-ik
date: 2026-07-09
type: result
title: Quantitative gait tracking on Shadow Hand (4 gaits, 40 s headless)
media: [media/manipulator-ik_gait-tracking.png]
---
Four gaits (cup, pinch, hybrid, multi-peak) run headless for 40 s each on the Shadow Hand in unified_v5, tracking object rotation via swing-twist quaternion decomposition at 8 ms resolution. The pinch gait achieves sustained rotation at 4.8 deg/s (72% of the kinematic no-slip target). Cup and multi-peak rotation is limited by a discrete friction-kick oscillation in the current sim architecture (the analytic torque impulse saturates at the Coulomb limit on alternating steps, producing near-zero net rotation). The hybrid gait escapes within 0.2 s due to AND-contact composition reducing the effective grip. These are comparative sim values, not predictive of physical rates. The friction-oscillation finding motivates planned implicit-friction integration.
