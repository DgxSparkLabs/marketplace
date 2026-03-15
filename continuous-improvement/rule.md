## Continuous Improvement

When asked to improve, harden, or make a codebase more robust and user-friendly, ALWAYS follow this seven-phase workflow. Do not skip phases. Complete each phase before moving to the next.

### Phase 1: Discovery

Systematically audit the codebase to find concrete improvement opportunities. NEVER guess — use tools to verify the real state of the code.

**What to look for:**

- **Code smells** — duplicated code, long functions (>40 lines), deep nesting (>3 levels), large classes, dead code, magic numbers, primitive obsession, feature envy
- **Error handling gaps** — missing try/catch at boundaries, swallowed errors, unhelpful error messages, no graceful degradation, unvalidated inputs, missing null/undefined checks
- **Edge cases** — empty inputs, zero/negative values, boundary conditions, concurrent access, timeout scenarios, Unicode/special characters, very large inputs
- **Security weaknesses** — hardcoded secrets, unsanitized user input, missing auth checks, overly broad permissions, dependency vulnerabilities
- **Usability friction** — unclear CLI output, missing help text, confusing error messages, no progress indicators for long operations, inconsistent naming
- **Missing tests** — untested public functions, no edge case coverage, no error path tests, missing integration tests for critical paths
- **Documentation gaps** — undocumented public APIs, missing setup instructions, stale README, no inline comments on complex logic
- **Performance issues** — N+1 queries, unnecessary re-renders, unbounded loops, missing pagination, large synchronous operations that should be async
- **Inconsistencies** — mixed naming conventions, inconsistent error handling patterns, style violations, inconsistent API response shapes

**How to discover:**

1. Read project structure and key entry points first
2. Trace the critical user-facing paths end to end
3. Run existing linters, type checkers, and test suites — read their output carefully
4. Search for known anti-patterns (`TODO`, `FIXME`, `HACK`, `XXX`, bare `except`, empty `catch`)
5. Check dependency health (outdated versions, known CVEs)
6. List every finding with file path, line number, and severity (critical/high/medium/low)

### Phase 2: Planning

Organize findings into a prioritized, actionable improvement plan. Present the plan to the user before implementing.

**Requirements:**

- Group findings by category (robustness, UX, tests, docs, performance, security)
- Rank by impact: critical fixes first, then high-value improvements, then polish
- For each item, state: what is wrong, why it matters, and what the fix looks like
- Estimate scope: single-line fix, function-level change, or multi-file refactor
- Identify dependencies between changes — order them so each step leaves the codebase working
- NEVER bundle unrelated changes together — each change should be reviewable in isolation
- Flag any changes that could break existing behavior or APIs

### Phase 3: Validation

Before implementing, verify that your assumptions are correct. NEVER refactor based on speculation.

**Checklist:**

- Confirm the problem actually exists by reproducing it or reading the code path
- Check if existing tests cover the area you plan to change — if they do, understand what they assert
- Verify that your proposed fix is compatible with the project's conventions, frameworks, and patterns
- Look at git history for the code you plan to change — understand why it was written that way
- If a change affects external behavior, confirm the current behavior first (run it, read tests, check docs)
- If unsure about intent, ask the user rather than assuming

### Phase 4: Implementation

Make changes methodically. Each change should be minimal, correct, and consistent with the existing codebase.

**Rules:**

- ALWAYS follow existing code conventions — match style, naming, patterns, and framework usage
- Change one thing at a time — do not mix refactors with feature changes or bug fixes
- Prefer simple, obvious solutions over clever ones — code is read far more than it is written
- When adding error handling, provide actionable error messages that tell the user what went wrong and how to fix it
- When improving UX, apply these principles:
  - Show system status: give feedback for every user action, especially long-running ones
  - Prevent errors: validate early, provide defaults, use confirmation for destructive actions
  - Use plain language: no jargon in user-facing messages, match the user's vocabulary
  - Be consistent: same action should produce same result everywhere
  - Support recovery: make operations reversible where possible, provide clear exit paths
- When hardening code:
  - Validate all external inputs at system boundaries
  - Handle all error paths explicitly — never silently swallow exceptions
  - Add timeouts to network calls and external process invocations
  - Use guard clauses to fail fast on invalid state
  - Replace magic numbers with named constants
- Do NOT over-engineer — solve the problem that exists now, not hypothetical future problems
- Do NOT remove or rewrite working code without a clear reason tied to a discovered problem

### Phase 5: Testing

Verify every change. NEVER mark an improvement as done without evidence it works.

**Requirements:**

- For every bug fix or behavior change, write or update a test that would have caught the original problem
- Run the full existing test suite after each logical group of changes — fix any regressions immediately
- For robustness improvements, add tests for the edge cases you identified (empty input, boundary values, error paths)
- For UX improvements, manually verify the output looks correct (run the CLI, check the messages, confirm formatting)
- If the project has linters or type checkers, run them and ensure zero new warnings
- If no test infrastructure exists, create a minimal test file to verify critical behavior, then offer to keep it
- Test both the happy path and failure modes — a change that only works when everything goes right is incomplete

### Phase 6: Documentation

Document what changed and why. Every improvement should be traceable.

**Requirements:**

- Update inline comments only where complex logic was added or changed — do not add obvious comments
- Update README or setup docs if installation steps, configuration, or usage changed
- If you added new public APIs, functions, or CLI flags, document their purpose and usage
- Write a clear commit message for each logical change: what changed, why, and what it fixes
- If the project has a CHANGELOG, update it
- If you created new conventions or patterns, document them in AGENTS.md or equivalent so future contributors follow them

### Phase 7: Self-Review

After testing and documentation, STOP and critically evaluate your own work before declaring done. Do not skip this — it is the difference between "technically complete" and "actually good."

**Ask yourself:**

- If I received this as a code review, would I approve it? Or would I request changes?
- Did I actually solve the root problem, or just patch a symptom?
- Is there anything I changed that I'm not fully confident about? If so, flag it to the user.
- Could any of my changes be simpler or clearer? Re-read each diff with fresh eyes.
- Did I introduce any new complexity, inconsistency, or technical debt?
- Are my error messages something a real user would understand and act on?
- Would a developer unfamiliar with this code understand my changes without extra explanation?

**If any answer is "no" or "I'm not sure":**

- Go back and fix it before proceeding. Do not hand off work you wouldn't accept yourself.
- If the fix requires significant rework, update the plan and re-run testing.
- If you're genuinely unsure whether something is good enough, tell the user what you're uncertain about and ask — don't silently ship doubt.

### Completion Checklist

Before declaring the improvement work done, verify ALL of the following:

- [ ] Every change addresses a real, discovered problem — no speculative changes
- [ ] All tests pass (existing + new)
- [ ] Linters and type checkers report no new issues
- [ ] No existing functionality was broken
- [ ] Error messages are actionable and user-friendly
- [ ] Code follows existing project conventions
- [ ] Changes are committed in logical, reviewable units
- [ ] Documentation is updated where relevant
- [ ] Self-review completed — you would approve this work if reviewing someone else's code
