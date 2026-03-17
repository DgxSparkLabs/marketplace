---
trigger: always_on
description: "Five-layer automated testing: compile, unit, integration, perf, e2e"
---

## Verification Ladder

Build automated verification at multiple layers. Set up test infrastructure before feature code.

### Layers
0. **Compile** — zero warnings (`-Wall -Wextra` or equivalent)
1. **Unit** — each function/API works correctly (PASS/FAIL/SKIP)
2. **Integration** — multiple functions compose correctly
3. **Performance** — baselines in machine-readable file, warn on >50% regression
4. **End-to-end** — real application smoke test, automated

### Principles
- Every test proves three things: correct **outcome**, correct **mechanism**, clean **side effects**.
- Test the negative path — invalid inputs must produce clean errors, not crashes.
- Distinguish PASS, FAIL, and SKIP — environment problems are SKIPs, not FAILs.
- Automate the most important check first.
- Pre-commit: build must succeed. Pre-push: fast test subset must pass.
