---
trigger: always_on
description: "Structured seven-phase workflow for codebase improvements"
---

## Continuous Improvement

When improving a codebase: **discover** (audit with tools, not guesses) → **plan** (rank by impact, one change per commit) → **validate** (confirm problems exist, check git history) → **implement** (match conventions, simple > clever) → **test** (happy path AND failure modes) → **document** → **self-review**.

Every session has two outputs: the work product and the process improvement.
- **Hit friction?** Fix the system — update a doc, improve a script. Don't just work around it.
- **Made a mistake?** Add a guardrail so the next agent can't repeat it.
- **Discovered something useful?** Write it in HANDOFF.md or AGENTS.md, not in conversation.
- **Are the rules wrong?** Fix them.
