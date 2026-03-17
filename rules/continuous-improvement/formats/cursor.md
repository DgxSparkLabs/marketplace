---
description: "Structured seven-phase workflow for codebase improvements"
alwaysApply: true
---

## Continuous Improvement

When asked to improve or harden a codebase, follow these phases in order:

1. **Discovery** — Audit for code smells, error handling gaps, edge cases, security issues, missing tests, docs gaps, performance problems. Use tools to verify — never guess. List findings with file path, line number, and severity.
2. **Planning** — Group by category, rank by impact, present plan before implementing. One change per commit. Flag anything that could break existing behavior.
3. **Validation** — Confirm each problem exists. Check existing tests. Read git history for context. Do not refactor based on speculation.
4. **Implementation** — Match existing conventions. One change at a time. Simple > clever. Do not over-engineer or rewrite working code without a discovered reason.
5. **Testing** — Write/update tests for every change. Run full suite after each group. Test happy path AND failure modes.
6. **Documentation** — Update docs where behavior changed. Clear commit messages.
7. **Self-review** — Would you approve this in code review? If unsure, fix it or flag it.
