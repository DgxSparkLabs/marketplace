## Blast Radius

Before making any change, estimate its blast radius — how many files it touches, how complex the diff will be, and how hard it is to revert.

- **Estimate first:** How many files? (>5 = break it up.) How complex? Can you revert cleanly?
- **Small atomic changes.** One commit = one purpose. Each independently revertable.
- **State your approach** in one sentence before coding. List files you expect to modify.
- **If >2x longer than expected**, STOP and reassess. Do not push through.
- **Simple > clever.** Do not build abstractions for one-time problems. When in doubt, do less.
- **Know your limits.** If the scope exceeds what fits in context, say so. Don't guess.
