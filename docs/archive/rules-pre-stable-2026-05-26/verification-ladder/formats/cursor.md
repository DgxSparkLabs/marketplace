---
description: "Five-layer automated testing: compile, unit, integration, perf, e2e"
alwaysApply: true
---

## Verification Ladder

Build automated verification at multiple layers. Set up test infrastructure before feature code.

**Layers:** compile (zero warnings) → unit → integration → performance (baseline file, warn on >50% regression) → end-to-end smoke test.

### Principles
- Every test proves three things: correct **outcome**, correct **mechanism**, clean **side effects**.
- Test the negative path — invalid inputs must produce clean errors, not crashes.
- Distinguish PASS, FAIL, and SKIP — environment problems are SKIPs, not FAILs.
- Automate the most important check first.
- Pre-commit: build must succeed. Pre-push: fast test subset must pass.
