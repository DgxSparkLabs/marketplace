---
description: "Scope changes by blast radius — prefer small atomic edits over large risky rewrites"
alwaysApply: true
---

## Blast Radius

Before any change, estimate blast radius — files touched, diff complexity, revertability.

- **Estimate first:** >5 files = break it up. Can you revert cleanly?
- **Small atomic changes.** One commit = one purpose. Each independently revertable.
- **State your approach** in one sentence before coding. List files you expect to modify.
- **If >2x longer than expected**, STOP and reassess. Do not push through.
- **Simple > clever.** Do not build abstractions for one-time problems. When in doubt, do less.
